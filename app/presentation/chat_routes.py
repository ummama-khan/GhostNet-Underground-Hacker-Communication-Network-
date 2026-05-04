from flask import Blueprint, request, jsonify
import datetime
import os
import html
import logging
from ..storage.database import load_data, save_data, MESSAGES_FILE
from ..application.security import token_required, require_role

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/messages/send', methods=['POST'])
@token_required
@require_role(['Member', 'Leader', 'Admin']) # Visitors cannot send messages
def send_message(current_user):
    data = request.json
    cell_id = data.get('cell_id')
    raw_content = data.get('content')
    ttl_minutes = data.get('ttl', 0)

    if not cell_id or not raw_content:
        return jsonify({"error": "Missing cell_id or content"}), 400

    # SECURITY CONTROL: Output Encoding / Input Sanitization
    safe_content = html.escape(raw_content)

    messages = load_data(MESSAGES_FILE)
    if cell_id not in messages["cells"]:
        messages["cells"][cell_id] = []

    expiry_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=int(ttl_minutes))).timestamp() if int(ttl_minutes) > 0 else 0

    msg_obj = {
        "id": os.urandom(8).hex(),
        "sender": current_user['username'],
        "content": safe_content, 
        "timestamp": datetime.datetime.utcnow().timestamp(),
        "expiry": expiry_time
    }

    messages["cells"][cell_id].append(msg_obj)
    save_data(MESSAGES_FILE, messages)
    
    logging.info(f"MESSAGE SENT: {current_user['username']} posted to {cell_id}")
    return jsonify({"message": "Message sent securely!"})

@chat_bp.route('/messages/<cell_id>', methods=['GET'])
@token_required
def get_messages(current_user, cell_id):
    messages = load_data(MESSAGES_FILE)
    
    if cell_id not in messages["cells"]:
        return jsonify({"messages": []})

    cell_msgs = messages["cells"][cell_id]
    current_time = datetime.datetime.utcnow().timestamp()
    
    # SECURITY CONTROL: Server-Side Logic Enforcement (TTL)
    active_messages = [
        msg for msg in cell_msgs 
        if msg['expiry'] == 0 or msg['expiry'] > current_time
    ]

    return jsonify({"messages": active_messages})