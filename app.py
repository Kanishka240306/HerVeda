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
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()  # reads variables from a .env file in this same folder, if present

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import firebase_admin
from firebase_admin import credentials, firestore, auth

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

# Used only to sign Flask's session cookie (keeps a user "logged in" between
# page loads). This is separate from Firebase Authentication itself.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me-before-deploying")

# Needed to verify email/password logins against Firebase Authentication.
# Find this in Firebase Console > Project Settings (gear icon) > General tab
# > "Web API Key". This is NOT the same as the service account key, and is
# safe to keep in code (it's the same key Firebase's own client SDKs use
# publicly in browsers) - but an env var is used here for tidiness.
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY", "")

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

# Public web config used by Firebase's client-side JS (for Google Sign-In).
# These values are NOT secret - they're the same config any Firebase web app
# embeds directly in its browser code. Find them in Firebase Console >
# Project Settings > General > Your apps > Config.
FIREBASE_CLIENT_CONFIG = {
    "apiKey": FIREBASE_WEB_API_KEY,
    "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", "herveda-88d0e.firebaseapp.com"),
    "projectId": os.environ.get("FIREBASE_PROJECT_ID", "herveda-88d0e"),
    "appId": os.environ.get("FIREBASE_APP_ID", "1:940618719589:web:056228514f89edb2d3418c"),
}


@app.context_processor
def inject_firebase_client_config():
    return {"firebase_config": FIREBASE_CLIENT_CONFIG}

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


# --- Real Firebase Authentication ---
# Account creation and password storage are now handled entirely by Firebase
# Authentication (not by our own code or Firestore). The `users` Firestore
# collection only holds extra profile info (name, goal) - never passwords.

def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("uid"):
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

    try:
        user_record = auth.create_user(
            email=email,
            password=password,
            display_name=name,
        )
    except auth.EmailAlreadyExistsError:
        return render_template(
            "signup.html", form_data=form_data,
            message="An account with this email already exists.", message_type="error"
        )
    except ValueError as e:
        # e.g. password too short (Firebase requires at least 6 characters)
        return render_template(
            "signup.html", form_data=form_data,
            message=f"Could not create account: {e}", message_type="error"
        )
    except Exception as e:
        app.logger.error(f"Firebase Auth signup error: {e}")
        return render_template(
            "signup.html", form_data=form_data,
            message="Something went wrong creating your account.", message_type="error"
        )

    # Profile info only - Firebase Auth already securely stores the password.
    db.collection(USERS_COLLECTION).document(user_record.uid).set({
        "name": name,
        "email": email,
        "goal": goal,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    })

    session["uid"] = user_record.uid
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

    if not FIREBASE_WEB_API_KEY:
        app.logger.error("FIREBASE_WEB_API_KEY is not set.")
        return render_template(
            "login.html", form_data=form_data,
            message="Server misconfiguration - contact the developer.", message_type="error"
        )

    # The Admin SDK (used elsewhere in this file) can create/manage users,
    # but only Firebase's own Identity Toolkit REST API can actually check
    # a password. This is the same request Firebase's client-side SDKs make.
    try:
        response = requests.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword",
            params={"key": FIREBASE_WEB_API_KEY},
            json={"email": email, "password": password, "returnSecureToken": True},
            timeout=10,
        )
    except requests.RequestException as e:
        app.logger.error(f"Could not reach Firebase Auth: {e}")
        return render_template(
            "login.html", form_data=form_data,
            message="Could not reach the login service. Try again.", message_type="error"
        )

    if response.status_code != 200:
        error_message = response.json().get("error", {}).get("message", "")
        if error_message in ("EMAIL_NOT_FOUND", "INVALID_PASSWORD", "INVALID_LOGIN_CREDENTIALS"):
            friendly_message = "Incorrect email or password."
        else:
            friendly_message = "Could not log in. Please try again."
        return render_template(
            "login.html", form_data=form_data,
            message=friendly_message, message_type="error"
        )

    result = response.json()
    uid = result["localId"]

    user_doc = db.collection(USERS_COLLECTION).document(uid).get()
    user_name = user_doc.to_dict().get("name", "") if user_doc.exists else ""

    session["uid"] = uid
    session["user_email"] = email
    session["user_name"] = user_name
    return redirect(url_for("dashboard"))


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/google-signin", methods=["POST"])
def google_signin():
    """
    Called by JS after a successful Google popup sign-in (see static/js/script.js).
    The browser gets a Firebase ID token from Google; we verify it here using
    the Admin SDK before trusting it and creating a session.
    """
    body = request.get_json(silent=True) or {}
    id_token = body.get("idToken", "")

    if not id_token:
        return jsonify(success=False, message="Missing sign-in token."), 400

    try:
        decoded_token = auth.verify_id_token(id_token)
    except Exception as e:
        app.logger.error(f"Google sign-in token verification failed: {e}")
        return jsonify(success=False, message="Could not verify Google sign-in."), 401

    uid = decoded_token["uid"]
    email = decoded_token.get("email", "")
    name = decoded_token.get("name", email.split("@")[0] if email else "")

    user_ref = db.collection(USERS_COLLECTION).document(uid)
    if not user_ref.get().exists:
        # First time this Google account has signed in - create a profile.
        # No "goal" yet since that only comes from the manual signup form.
        user_ref.set({
            "name": name,
            "email": email,
            "goal": "",
            "createdAt": datetime.now(timezone.utc).isoformat(),
        })

    session["uid"] = uid
    session["user_email"] = email
    session["user_name"] = name
    return jsonify(success=True, redirect=url_for("dashboard"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        form_data = request.form
        db.collection(CHECK_INS_COLLECTION).add({
            "userId": session["uid"],
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
            "userId": session["uid"],
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
            "userId": session["uid"],
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
            "userId": session["uid"],
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