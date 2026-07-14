import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

USERS_FILE = os.path.join(PROJECT_DIR, "hospital_users.json")

DEFAULT_USERS = {
    "admin": {"password": "admin123", "role": "Administrator", "full_name": "Admin User"},
    "doctor": {"password": "doc456", "role": "Doctor", "full_name": "Dr. Kamau"},
    "nurse": {"password": "nurse789", "role": "Nurse", "full_name": "Nurse Achieng"},
    "reception": {"password": "rec000", "role": "HRIO", "full_name": "Faith Mwangi"},
    "pharma": {"password": "pharm111", "role": "Pharmacist", "full_name": "Peter Otieno"},
    "morgue": {"password": "morgue123", "role": "Morgue Attendant", "full_name": "John Doe"},
}

ROLES = [
    "Administrator",
    "Doctor",
    "Nurse",
    "HRIO",
    "Pharmacist",
    "Resident/Intern",
    "Lab Technician",
    "Radiologic Technologist",
    "Respiratory Therapist",
    "Physical Therapist",
    "Dietitian",
    "Social Worker",
    "Case Manager",
    "Morgue Attendant",
]


def _load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
    return dict(DEFAULT_USERS)


def _save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True})

    @app.post("/api/login")
    def login():
        payload = request.get_json(silent=True) or {}
        username = str(payload.get("username", "")).strip().lower()
        password = str(payload.get("password", ""))

        if not username or not password:
            return jsonify({"ok": False, "error": "username and password are required"}), 400

        users = _load_users()
        user = users.get(username)
        if not user or user.get("password") != password:
            return jsonify({"ok": False, "error": "Invalid username or password"}), 401

        return jsonify({"ok": True, "username": username, "role": user.get("role")})

    @app.post("/api/signup")
    def signup():
        payload = request.get_json(silent=True) or {}
        full_name = str(payload.get("fullName", "")).strip()
        username = str(payload.get("username", "")).strip().lower()
        role = str(payload.get("role", "")).strip() or "Nurse"
        password = str(payload.get("password", ""))
        confirm = str(payload.get("confirmPassword", ""))

        if not full_name or not username:
            return jsonify({"ok": False, "error": "fullName and username are required"}), 400
        if len(username) < 3:
            return jsonify({"ok": False, "error": "username must be at least 3 characters"}), 400
        if role not in ROLES:
            return jsonify({"ok": False, "error": f"role must be one of: {', '.join(ROLES)}"}), 400
        if len(password) < 6:
            return jsonify({"ok": False, "error": "password must be at least 6 characters"}), 400
        if password != confirm:
            return jsonify({"ok": False, "error": "passwords do not match"}), 400

        users = _load_users()
        if username in users:
            return jsonify({"ok": False, "error": "username already taken"}), 400

        users[username] = {"password": password, "role": role, "full_name": full_name}
        _save_users(users)

        return jsonify({"ok": True, "username": username, "role": role})

    return app


app = create_app()

if __name__ == "__main__":
    # Run: python backend/app.py
    app.run(host="127.0.0.1", port=5000, debug=True)

