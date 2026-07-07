"""
HerVeda backend - Flask version
Replicates the behavior of server.js:
 - Serves the static frontend (index.html, style.css, script.js, etc.)
 - POST /waitlist   -> validates email (syntax + real DNS domain check), stores to waitlist.json
 - GET  /health     -> simple health check
"""

import json
import os
import socket
import re
from datetime import datetime, timezone

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "waitlist.json")
PORT = int(os.environ.get("PORT", 3000))

# Only these origins are allowed to call this API from a browser.
# Add your real deployed frontend domain here once you deploy.
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"), template_folder=os.path.join(BASE_DIR, "templates"))

# Lock down CORS to only the origins listed above (instead of "*")
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

# Rate limiting: caps requests per IP address to prevent spam/abuse
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

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


def read_waitlist():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def write_waitlist(waitlist):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(waitlist, f, indent=2)


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
        current_waitlist = read_waitlist()
    except Exception as e:
        app.logger.error(f"Unable to read waitlist file: {e}")
        return jsonify(success=False, message="Server error reading data."), 500

    if any(entry.get("email") == trimmed_email for entry in current_waitlist):
        return jsonify(success=False, message="This email is already on the waitlist."), 409

    entry = {
        "email": trimmed_email,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    current_waitlist.append(entry)

    try:
        write_waitlist(current_waitlist)
    except Exception as e:
        app.logger.error(f"Unable to save waitlist entry: {e}")
        return jsonify(success=False, message="Server error saving data."), 500

    return jsonify(success=True, message="Thank you! We will be in touch soon.")


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok", service="Herveda backend")


def render_with_message(template_name, form_data=None, message=None, message_type="info"):
    return render_template(
        template_name,
        form_data=form_data or {},
        message=message,
        message_type=message_type,
    )


@app.route("/", methods=["GET"])
def landing():
    return render_with_message("landing.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "goal": request.form.get("goal", "").strip(),
        }
        if not form_data["name"] or not form_data["email"] or not request.form.get("password", "").strip():
            return render_with_message("signup.html", form_data=form_data, message="Please complete all fields to create your account.", message_type="error")

        return render_with_message("signup.html", form_data=form_data, message="Account created successfully. Welcome to HerVeda!", message_type="success")

    return render_with_message("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_data = {
            "email": request.form.get("email", "").strip(),
        }
        if not form_data["email"] or not request.form.get("password", "").strip():
            return render_with_message("login.html", form_data=form_data, message="Please enter your email and password.", message_type="error")

        return render_with_message("login.html", form_data=form_data, message="You are logged in. Welcome back!", message_type="success")

    return render_with_message("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        form_data = {
            "mood": request.form.get("mood", "").strip(),
            "note": request.form.get("note", "").strip(),
        }
        if not form_data["mood"]:
            return render_with_message("dashboard.html", form_data=form_data, message="Please select how you are feeling.", message_type="error")

        return render_with_message("dashboard.html", form_data=form_data, message="Your check-in has been saved.", message_type="success")

    return render_with_message("dashboard.html")


@app.route("/cycle-tracker", methods=["GET", "POST"])
def cycle_tracker():
    if request.method == "POST":
        form_data = {
            "date": request.form.get("date", "").strip(),
            "flow": request.form.get("flow", "").strip(),
            "symptoms": request.form.get("symptoms", "").strip(),
        }
        if not form_data["date"]:
            return render_with_message("cycle_tracker.html", form_data=form_data, message="Please choose a date for your tracker entry.", message_type="error")

        return render_with_message("cycle_tracker.html", form_data=form_data, message="Your cycle entry has been saved.", message_type="success")

    return render_with_message("cycle_tracker.html")


@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    if request.method == "POST":
        form_data = {
            "energy": request.form.get("energy", "").strip(),
            "stress": request.form.get("stress", "").strip(),
            "notes": request.form.get("notes", "").strip(),
        }
        return render_with_message("assessment.html", form_data=form_data, message="Thanks for sharing your wellbeing update.", message_type="success")

    return render_with_message("assessment.html")


@app.route("/daily-plan", methods=["GET", "POST"])
def daily_plan():
    if request.method == "POST":
        form_data = {
            "focus": request.form.get("focus", "").strip(),
            "action": request.form.get("action", "").strip(),
            "reminder": request.form.get("reminder", "").strip(),
        }
        if not form_data["focus"] or not form_data["action"]:
            return render_with_message("daily_plan.html", form_data=form_data, message="Please add a focus and a self-care action.", message_type="error")

        return render_with_message("daily_plan.html", form_data=form_data, message="Your daily plan is ready.", message_type="success")

    return render_with_message("daily_plan.html")


if __name__ == "__main__":
    print(f"Herveda backend running at http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)