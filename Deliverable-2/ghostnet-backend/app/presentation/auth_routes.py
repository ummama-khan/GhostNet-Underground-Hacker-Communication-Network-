from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import logging
from ..storage.database import load_data, save_data, USERS_FILE
from ..application.security import SECRET_KEY
from ..extensions import limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    users = load_data(USERS_FILE)
    if username in users:
        return jsonify({"error": "User already exists"}), 400

    # SECURITY CONTROL: Prevent Privilege Escalation (Mass Assignment)
    assigned_role = "Visitor"
    
    # SECURITY CONTROL: Secure Authentication (Password Hashing)
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    users[username] = {"password": hashed_password, "role": assigned_role}
    save_data(USERS_FILE, users)
    
    logging.info(f"USER REGISTERED: {username} with role {assigned_role}")
    return jsonify({"message": "Registration successful!"}), 201
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute") # SECURITY CONTROL: Rate Limiting
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    generic_error = {"error": "Invalid username or password"}

    users = load_data(USERS_FILE)
    user = users.get(username)

    if not user or not check_password_hash(user['password'], password):
        logging.warning(f"LOGIN FAILED: Attempt for username '{username}'")
        return jsonify(generic_error), 401

    token = jwt.encode({
        'username': username,
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    logging.info(f"LOGIN SUCCESS: {username}")
    return jsonify({"token": token, "role": user['role']})