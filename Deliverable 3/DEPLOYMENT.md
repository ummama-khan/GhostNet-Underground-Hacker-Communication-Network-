# GhostNet System Deployment Guide

### Prerequisites
* Python 3.12+
* Google Chrome (Recommended)

### Step 1: Backend Setup
1. Open a terminal in the `ghostnet-backend` folder.
2. Activate the environment:
   ```powershell
   .\.venv\Scripts\activate
3. Install dependencies:

PowerShell
pip install -r requirements.txt

4. Reset/Seed the Database:
   ```powershell
   python reset_db.py
   (Type 'y' to confirm. This creates the Admin account).


 ### Step 2: Running the System
1. Start the Flask server:

PowerShell
python run.py

2. Open `ghostnet-frontend/index.html` in your browser.

### Step 3: Admin Access & Security Testing
* **Credentials:** `overwatch_admin` / `admin123`
* **TTL Feature:** Set message TTL to `1` (minute). Send a message, wait 60 seconds, and click **Refresh** to verify auto-deletion.
* **Audit:** Run `bandit -r app/` to verify security compliance.