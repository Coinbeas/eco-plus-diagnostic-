from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import os


app = Flask(__name__)

# =========================================
# Configuration
# =========================================

app.config["JSON_AS_ASCII"] = False


# Temporary in-memory appointment storage.
# Production version should use MySQL/PostgreSQL.
appointments = []


# =========================================
# Home Page
# =========================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================
# Health Check
# =========================================

@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "status": "healthy",
        "service": "ECO Plus Diagnostic Center",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


# =========================================
# Appointment API
# =========================================

@app.route("/api/appointments", methods=["POST"])
def create_appointment():

    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    service = str(data.get("service", "")).strip()


    # -----------------------------
    # Validation
    # -----------------------------

    if not name:
        return jsonify({
            "success": False,
            "message": "আপনার নাম দিন।"
        }), 400


    if not phone:
        return jsonify({
            "success": False,
            "message": "মোবাইল নম্বর দিন।"
        }), 400


    if not service:
        return jsonify({
            "success": False,
            "message": "একটি সেবা নির্বাচন করুন।"
        }), 400


    # -----------------------------
    # Create appointment
    # -----------------------------

    appointment = {
        "id": len(appointments) + 1,
        "name": name,
        "phone": phone,
        "service": service,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "status": "new"
    }


    appointments.append(appointment)


    return jsonify({
        "success": True,
        "message": "আপনার Appointment Request সফলভাবে পাঠানো হয়েছে।",
        "appointment": appointment
    }), 201


# =========================================
# Appointment List
# Temporary Admin/API testing endpoint
# =========================================

@app.route("/api/appointments", methods=["GET"])
def get_appointments():

    return jsonify({
        "success": True,
        "count": len(appointments),
        "appointments": appointments
    })


# =========================================
# Admin Login Page
# =========================================

@app.route("/admin/login")
def admin_login():

    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Admin Login - ECO Plus</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;

                display: flex;
                align-items: center;
                justify-content: center;

                padding: 20px;

                font-family:
                    system-ui,
                    -apple-system,
                    "Segoe UI",
                    sans-serif;

                background: #f1f5f9;
                color: #0f172a;
            }

            .login-card {
                width: 100%;
                max-width: 420px;

                padding: 30px;

                background: white;
                border-radius: 20px;

                box-shadow:
                    0 15px 40px
                    rgba(15, 23, 42, 0.12);
            }

            h1 {
                margin-top: 0;
                font-size: 1.6rem;
            }

            p {
                color: #64748b;
            }

            .notice {
                margin-top: 20px;
                padding: 14px;

                border-radius: 12px;

                background: #fef3c7;
                color: #92400e;

                font-size: 0.9rem;
            }

            a {
                display: inline-block;
                margin-top: 20px;

                color: #0f766e;
                font-weight: 700;
                text-decoration: none;
            }
        </style>
    </head>

    <body>

        <main class="login-card">

            <h1>🔐 Admin Portal</h1>

            <p>
                ECO Plus Diagnostic Center
            </p>

            <div class="notice">
                Admin authentication will be connected
                in the production backend.
            </div>

            <a href="/">
                ← Back to Website
            </a>

        </main>

    </body>
    </html>
    """


# =========================================
# 404 Handler
# =========================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "message": "Resource not found."
    }), 404


# =========================================
# Application Entry Point
# =========================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
