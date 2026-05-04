from flask import Blueprint, request, jsonify
from models import Admin
from extensions import db, bcrypt
from flask_login import login_user, logout_user

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if Admin.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Account already exists"}), 400

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

    login_user(user)
    return jsonify({"message": "Login successful"})

@auth.route("/logout")
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})
