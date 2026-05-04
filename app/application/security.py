import jwt
from flask import request, jsonify, current_app
from functools import wraps
import logging
from ..storage.database import AUDIT_LOG_FILE



# SECURITY CONTROL: Session Security (Tokens)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            token = token.split(" ")[1] # Format expects: "Bearer <token>"
            data = jwt.decode(token,current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except Exception:
            return jsonify({'error': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# SECURITY CONTROL: RBAC Enforcement (Deny-by-default)
def require_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user['role'] not in allowed_roles:
                logging.warning(f"ACCESS DENIED: {current_user['username']} attempted restricted access.")
                return jsonify({'error': 'Unauthorized: Insufficient privileges'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator