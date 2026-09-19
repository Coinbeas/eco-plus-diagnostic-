from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "eco-plus-diagnostic-secret-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@ecoplus.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

appointments = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip().lower()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        identifier = username or email
        if (identifier in {ADMIN_USERNAME.lower(), ADMIN_EMAIL.lower()} and password == ADMIN_PASSWORD):
            session["admin_logged_in"] = True
            session["admin_username"] = ADMIN_USERNAME
            return redirect(url_for("admin_dashboard"))

        error = "Invalid username/email or password."

    return render_template("admin-login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin-dashboard.html", appointments=appointments)


@app.route("/api/appointments", methods=["POST"])
def appointments_api():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    service = (data.get("service") or "").strip()

    if not name or not phone or not service:
        return jsonify({"message": "সব তথ্য পূরণ করুন।"}), 400

    appointments.append({
        "name": name,
        "phone": phone,
        "service": service,
        "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    })

    return jsonify({
        "message": "✅ আপনার Appointment Request সফলভাবে পাঠানো হয়েছে।"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
