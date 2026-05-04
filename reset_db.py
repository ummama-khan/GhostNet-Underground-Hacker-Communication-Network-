import os
import json
from werkzeug.security import generate_password_hash

# Define paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'app', 'storage', 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')

def reset_database():
    print("⚠️ Initiating GhostNet Database Wipe...")
    
    # 1. Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # 2. Define the Seed Users (The "Overwatch" Admin and a test Member)
    seed_users = {
        "overwatch_admin": {
            "password": generate_password_hash("admin123", method='pbkdf2:sha256'),
            "role": "Admin"
        },
        "test_agent": {
            "password": generate_password_hash("agent123", method='pbkdf2:sha256'),
            "role": "Member"
        }
    }

    # 3. Wipe and rewrite users.json
    with open(USERS_FILE, 'w') as f:
        json.dump(seed_users, f, indent=4)
    print("✅ users.json wiped and seeded with default Admin.")

    # 4. Wipe and rewrite messages.json (empty list)
    with open(MESSAGES_FILE, 'w') as f:
        json.dump([], f, indent=4)
    print("✅ messages.json wiped clean.")

    print("🚀 Database reset complete. You can now log in with 'overwatch_admin' and 'admin123'.")

if __name__ == "__main__":
    # Add a quick safety prompt so you don't accidentally wipe it later
    confirm = input("Are you sure you want to completely wipe the database? (y/n): ")
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("Reset aborted.")