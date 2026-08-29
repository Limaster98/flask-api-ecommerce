from flask import Blueprint, request, jsonify
from flask_login import login_required, logout_user, login_user
from models import User

users_route = Blueprint('user',__name__)

@users_route.route('/login', methods=['POST'])
def login():
    login_data = request.json
    user = User.query.filter_by(username=login_data.get('username')).first()
    if user and user.password == login_data.get('password'):
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@users_route.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout succesfully"})