from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin/login")
def admin_login():
    return "<h1>Admin Login</h1><p>Coming soon.</p>"


@app.route("/api/appointments", methods=["POST"])
def appointments():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    service = (data.get("service") or "").strip()

    if not name or not phone or not service:
        return jsonify({"message": "সব তথ্য পূরণ করুন।"}), 400

    return jsonify({
        "message": "✅ আপনার Appointment Request সফলভাবে পাঠানো হয়েছে।"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
