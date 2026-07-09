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

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
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

# Flask now uses its default conventions: templates/ folder for pages,
# static/ folder for CSS/JS. (Previously this pointed at BASE_DIR directly,
# which conflicted with Kanishka's templates/static folder structure.)
app = Flask(__name__)

# TEMPORARY: used only to sign session cookies for the login stopgap below.
# Once real Firebase Authentication (task #4) is wired in, this session-based
# login can be replaced with Firebase ID token verification instead.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me-before-deploying")

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
USERS_COLLECTION = "users"
CYCLE_LOGS_COLLECTION = "cycleLogs"
ASSESSMENTS_COLLECTION = "symptomAssessments"
DAILY_PLANS_COLLECTION = "dailyPlans"
CHECK_INS_COLLECTION = "checkIns"

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


# --- Login stopgap (temporary, until task #4 real Firebase Auth) ---
# Passwords ARE properly hashed (never stored in plain text), but this is
# still a simplified stand-in for real authentication. It exists so the
# rest of the app (cycle tracker, assessment, daily plan) has something to
# tie data to right now. Swap this out for Firebase Auth ID token
# verification when task #4 is built.

def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("user_email"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped


@app.route("/", methods=["GET"])
def landing():
    return render_template("landing.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", form_data={})

    form_data = request.form
    name = form_data.get("name", "").strip()
    email = form_data.get("email", "").strip().lower()
    password = form_data.get("password", "")
    goal = form_data.get("goal", "")

    if not name or not email or not password:
        return render_template(
            "signup.html", form_data=form_data,
            message="Please fill in all required fields.", message_type="error"
        )

    user_ref = db.collection(USERS_COLLECTION).document(email)
    if user_ref.get().exists:
        return render_template(
            "signup.html", form_data=form_data,
            message="An account with this email already exists.", message_type="error"
        )

    user_ref.set({
        "name": name,
        "email": email,
        "goal": goal,
        "passwordHash": generate_password_hash(password),
        "createdAt": datetime.now(timezone.utc).isoformat(),
    })

    session["user_email"] = email
    session["user_name"] = name
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", form_data={})

    form_data = request.form
    email = form_data.get("email", "").strip().lower()
    password = form_data.get("password", "")

    user_doc = db.collection(USERS_COLLECTION).document(email).get()
    if not user_doc.exists:
        return render_template(
            "login.html", form_data=form_data,
            message="No account found with that email.", message_type="error"
        )

    user = user_doc.to_dict()
    if not check_password_hash(user.get("passwordHash", ""), password):
        return render_template(
            "login.html", form_data=form_data,
            message="Incorrect password.", message_type="error"
        )

    session["user_email"] = email
    session["user_name"] = user.get("name", "")
    return redirect(url_for("dashboard"))


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        form_data = request.form
        db.collection(CHECK_INS_COLLECTION).add({
            "userId": session["user_email"],
            "mood": form_data.get("mood", ""),
            "note": form_data.get("note", ""),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        })
        return render_template(
            "dashboard.html", form_data={},
            message="Check-in saved.", message_type="success"
        )
    return render_template("dashboard.html", form_data={})


@app.route("/cycle-tracker", methods=["GET", "POST"])
@login_required
def cycle_tracker():
    if request.method == "POST":
        form_data = request.form
        db.collection(CYCLE_LOGS_COLLECTION).add({
            "userId": session["user_email"],
            "date": form_data.get("date", ""),
            "flow": form_data.get("flow", ""),
            "symptoms": form_data.get("symptoms", ""),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        })
        return render_template(
            "cycle_tracker.html", form_data={},
            message="Entry saved.", message_type="success"
        )
    return render_template("cycle_tracker.html", form_data={})


@app.route("/assessment", methods=["GET", "POST"])
@login_required
def assessment():
    if request.method == "POST":
        form_data = request.form
        db.collection(ASSESSMENTS_COLLECTION).add({
            "userId": session["user_email"],
            "energy": form_data.get("energy", ""),
            "stress": form_data.get("stress", ""),
            "notes": form_data.get("notes", ""),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        })
        return render_template(
            "assessment.html", form_data={},
            message="Assessment submitted.", message_type="success"
        )
    return render_template("assessment.html", form_data={})


@app.route("/daily-plan", methods=["GET", "POST"])
@login_required
def daily_plan():
    if request.method == "POST":
        form_data = request.form
        db.collection(DAILY_PLANS_COLLECTION).add({
            "userId": session["user_email"],
            "focus": form_data.get("focus", ""),
            "action": form_data.get("action", ""),
            "reminder": form_data.get("reminder", ""),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        })
        return render_template(
            "daily_plan.html", form_data={},
            message="Plan saved.", message_type="success"
        )
    return render_template("daily_plan.html", form_data={})


if __name__ == "__main__":
    print(f"Herveda backend running at http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)