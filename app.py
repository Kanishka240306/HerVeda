"""
HerVeda backend - Flask version
 - Serves the static frontend (index.html, style.css, script.js, etc.)
 - POST /waitlist   -> validates email (syntax + real DNS domain check), stores to Firestore
 - GET  /health     -> simple health check

Data is stored in Firestore (Google Cloud) instead of a local JSON file.
Requires firebase-service-account.json in the same folder as this file
(never commit this file to git - it's a secret admin credential).
"""

import os
import socket
import re
from datetime import datetime, timezone

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import firebase_admin
from firebase_admin import credentials, firestore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "firebase-service-account.json")
PORT = int(os.environ.get("PORT", 3000))

# Only these origins are allowed to call this API from a browser.
# Add your real deployed frontend domain here once you deploy.
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")

# Lock down CORS to only the origins listed above (instead of "*")
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

# Rate limiting: caps requests per IP address to prevent spam/abuse
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# --- Firebase / Firestore setup ---
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    raise RuntimeError(
        "firebase-service-account.json not found. "
        "Download it from Firebase Console > Project Settings > Service Accounts, "
        "and place it in the same folder as app.py."
    )

cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)
db = firestore.client()
WAITLIST_COLLECTION = "waitlist"

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_email_syntax_valid(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email))


def has_valid_email_domain(domain: str) -> bool:
    """
    Mirrors the Node version's logic:
    1. Try MX records first (mail servers for the domain)
    2. Fall back to A / AAAA records (domain resolves at all)
    """
    try:
        import dns.resolver  # provided by the dnspython package

        try:
            answers = dns.resolver.resolve(domain, "MX")
            if answers and len(answers) > 0:
                return True
        except Exception:
            pass  # fall through to A/AAAA check

        try:
            answers = dns.resolver.resolve(domain, "A")
            if answers and len(answers) > 0:
                return True
        except Exception:
            pass

        try:
            answers = dns.resolver.resolve(domain, "AAAA")
            return bool(answers and len(answers) > 0)
        except Exception:
            return False

    except ImportError:
        # Fallback if dnspython isn't installed: basic hostname resolution only
        # (won't check MX records, just whether the domain resolves at all)
        try:
            socket.getaddrinfo(domain, None)
            return True
        except socket.gaierror:
            return False


def waitlist_entry_exists(email: str) -> bool:
    doc = db.collection(WAITLIST_COLLECTION).document(email).get()
    return doc.exists


def save_waitlist_entry(email: str):
    """
    Uses the email itself as the Firestore document ID.
    This makes duplicate-prevention atomic and race-safe (unlike the old
    JSON file approach, where two simultaneous submissions could both read
    the file before either had written, silently losing one entry).
    """
    db.collection(WAITLIST_COLLECTION).document(email).set({
        "email": email,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    })


@app.route("/waitlist", methods=["POST"])
@limiter.limit("5 per minute")
def waitlist():
    body = request.get_json(silent=True) or {}
    email = body.get("email", "")
    trimmed_email = email.strip().lower() if isinstance(email, str) else ""

    if not trimmed_email:
        return jsonify(success=False, message="Please enter your email address."), 400

    if not is_email_syntax_valid(trimmed_email):
        return jsonify(success=False, message="Please enter a valid email address."), 400

    parts = trimmed_email.split("@")
    domain = parts[1] if len(parts) == 2 else ""
    if not domain:
        return jsonify(success=False, message="Please enter a valid email address."), 400

    if not has_valid_email_domain(domain):
        return jsonify(success=False, message="Email domain does not appear to be valid."), 400

    try:
        already_exists = waitlist_entry_exists(trimmed_email)
    except Exception as e:
        app.logger.error(f"Unable to check Firestore for existing entry: {e}")
        return jsonify(success=False, message="Server error reading data."), 500

    if already_exists:
        return jsonify(success=False, message="This email is already on the waitlist."), 409

    try:
        save_waitlist_entry(trimmed_email)
    except Exception as e:
        app.logger.error(f"Unable to save waitlist entry to Firestore: {e}")
        return jsonify(success=False, message="Server error saving data."), 500

    return jsonify(success=True, message="Thank you! We will be in touch soon.")


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok", service="Herveda backend")


@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory(BASE_DIR, "index.html")


if __name__ == "__main__":
    print(f"Herveda backend running at http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)