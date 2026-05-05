import json
import os
import logging

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')
AUDIT_LOG_FILE = os.path.join(DATA_DIR, 'audit.log')

# Initialize directories and files if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f: json.dump({}, f)
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f: json.dump({"cells": {}}, f)

# SECURITY CONTROL: Audit Logging Setup
logging.basicConfig(
    filename=AUDIT_LOG_FILE, 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_data(filepath):
    with open(filepath, 'r') as f: 
        return json.load(f)

def save_data(filepath, data):
    with open(filepath, 'w') as f: 
        json.dump(data, f, indent=4)