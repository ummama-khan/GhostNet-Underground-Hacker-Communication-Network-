from flask import Blueprint, request, jsonify
import logging
from ..storage.database import load_data, save_data, USERS_FILE
from ..application.security import token_required, require_role

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/promote', methods=['POST'])
@token_required
@require_role(['Admin']) # SECURITY CONTROL: Strict Privilege Authorization
def promote_user(current_user):
    data = request.json
    target_user = data.get('username')
    new_role = data.get('role')

    if new_role not in ['Visitor', 'Member', 'Leader', 'Admin']:
        return jsonify({"error": "Invalid role"}), 400

    users = load_data(USERS_FILE)
    if target_user in users:
        users[target_user]['role'] = new_role
        save_data(USERS_FILE, users)
        
        logging.info(f"ROLE UPDATE: Admin '{current_user['username']}' promoted '{target_user}' to {new_role}")
        return jsonify({"message": f"{target_user} promoted to {new_role}"})

    return jsonify({"error": "User not found"}), 404