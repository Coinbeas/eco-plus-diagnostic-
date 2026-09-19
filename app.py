from datetime import datetime, timezone
from functools import wraps
import os
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "eco-plus-diagnostic-secret-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("COOKIE_SECURE", "0") == "1"

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@ecoplus.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    os.path.join(app.instance_path, "appointments.db"),
)

# Ensure both the Flask instance directory and a custom disk path are writable.
os.makedirs(app.instance_path, exist_ok=True)
database_directory = os.path.dirname(os.path.abspath(DATABASE_PATH))
os.makedirs(database_directory, exist_ok=True)


def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


init_db()


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == "POST":
        identifier = (request.form.get("username") or "").strip().lower()
        password = request.form.get("password") or ""

        valid_identifier = identifier in {
            ADMIN_USERNAME.lower(),
            ADMIN_EMAIL.lower(),
        }
        if valid_identifier and password == ADMIN_PASSWORD:
            session.clear()
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
@admin_required
def admin_dashboard():
    with get_db() as connection:
        rows = connection.execute(
            "SELECT id, name, phone, service, created_at "
            "FROM appointments ORDER BY id DESC"
        ).fetchall()

        today = datetime.now(timezone.utc).date().isoformat()
        today_count = connection.execute(
            "SELECT COUNT(*) FROM appointments WHERE substr(created_at, 1, 10) = ?",
            (today,),
        ).fetchone()[0]

    return render_template(
        "admin-dashboard.html",
        appointments=rows,
        today_count=today_count,
    )


@app.route("/api/appointments", methods=["POST"])
def appointments_api():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    service = (data.get("service") or "").strip()

    if not name or not phone or not service:
        return jsonify({"message": "সব তথ্য পূরণ করুন।"}), 400

    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    with get_db() as connection:
        connection.execute(
            "INSERT INTO appointments (name, phone, service, created_at) "
            "VALUES (?, ?, ?, ?)",
            (name, phone, service, created_at),
        )
        connection.commit()

    return jsonify({
        "message": "✅ আপনার Appointment Request সফলভাবে পাঠানো হয়েছে।"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
