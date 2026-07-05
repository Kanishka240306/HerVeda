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

from flask import Flask, request, jsonify, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "waitlist.json")
PORT = int(os.environ.get("PORT", 3000))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")

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


@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory(BASE_DIR, "index.html")


if __name__ == "__main__":
    print(f"Herveda backend running at http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)