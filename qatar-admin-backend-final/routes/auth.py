from flask import Blueprint, request, jsonify
from models import Admin
from extensions import db, bcrypt
from flask_login import login_user, logout_user
from itsdangerous import URLSafeTimedSerializer
from config import Config

auth = Blueprint("auth", __name__)
serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if Admin.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Account already exists"}), 400
    if len(data["password"]) < 8 or data["password"] != data["confirm_password"]:
        return jsonify({"error": "Invalid password"}), 400

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode()
    user = Admin(full_name=data["full_name"], email=data["email"], password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Signup successful"})

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    user = Admin.query.filter_by(email=data["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
    login_user(user, remember=data.get("remember", False))
    return jsonify({"message": "Login successful"})

@auth.route("/logout")
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

@auth.route("/forgot-password", methods=["POST"])
def forgot():
    data = request.json
    user = Admin.query.filter_by(email=data["email"]).first()
    if user:
        token = serializer.dumps(user.email, salt="reset")
        print(f"RESET LINK: http://localhost:5000/reset/{token}")
    return jsonify({"message": "If the email exists, a reset link has been sent"})

@auth.route("/reset/<token>", methods=["POST"])
def reset(token):
    try:
        email = serializer.loads(token, salt="reset", max_age=3600)
    except:
        return jsonify({"error": "Token expired"}), 400
    data = request.json
    user = Admin.query.filter_by(email=email).first()
    user.password = bcrypt.generate_password_hash(data["password"]).decode()
    db.session.commit()
    return jsonify({"message": "Password reset successful"})
