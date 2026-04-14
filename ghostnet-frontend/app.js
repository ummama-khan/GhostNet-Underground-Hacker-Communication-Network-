const API_BASE = 'http://127.0.0.1:5000/api';

// Helper function to show messages on screen
function showSystemMessage(msg) {
    document.getElementById('system-messages').innerText = msg;
    setTimeout(() => { document.getElementById('system-messages').innerText = ''; }, 3000);
}

// --- AUTHENTICATION ---

async function register() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;

    const response = await fetch(`${API_BASE}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass }) // Backend forces 'Visitor' role
    });

    const data = await response.json();
    if (response.ok) {
        showSystemMessage("Registration successful. You may now login.");
    } else {
        showSystemMessage("Error: " + data.error);
    }
}

async function login() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;

    const response = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    });

    const data = await response.json();
    if (response.ok) {
        // Save token to browser's Local Storage
        localStorage.setItem('ghostnet_token', data.token);
        localStorage.setItem('ghostnet_username', user);
        localStorage.setItem('ghostnet_role', data.role);
        
        showSystemMessage("Access Granted.");
        loadChatInterface();
    } else {
        showSystemMessage("Error: " + data.error);
    }
}

function logout() {
    localStorage.removeItem('ghostnet_token');
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('chat-section').classList.add('hidden');
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    showSystemMessage("Disconnected.");
}

// --- UI TOGGLES ---

function loadChatInterface() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('chat-section').classList.remove('hidden');
    
    document.getElementById('current-user').innerText = localStorage.getItem('ghostnet_username');
    document.getElementById('current-role').innerText = localStorage.getItem('ghostnet_role');
}

// Check if already logged in when page refreshes
window.onload = () => {
    if (localStorage.getItem('ghostnet_token')) {
        loadChatInterface();
    }
};
// --- CHAT FUNCTIONALITY ---

async function fetchMessages() {
    const token = localStorage.getItem('ghostnet_token');
    // Grab the currently selected cell from the dropdown
    const activeCell = document.getElementById('cell-selector').value; 
    
    const response = await fetch(`${API_BASE}/messages/${activeCell}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}` 
        }
    });

    const data = await response.json();
    if (response.ok) {
        const display = document.getElementById('messages-display');
        display.innerHTML = ''; 

        if (data.messages.length === 0) {
            display.innerHTML = '<p style="color: #555;">[ No active messages in this cell ]</p>';
            return;
        }

        data.messages.forEach(msg => {
            const timeStr = new Date(msg.timestamp * 1000).toLocaleTimeString();
            display.innerHTML += `
                <div style="margin-bottom: 8px; border-bottom: 1px solid #222; padding-bottom: 4px;">
                    <span style="color: #666;">[${timeStr}]</span> 
                    <strong style="color: #00ffff;">${msg.sender}:</strong> 
                    <span style="color: #eee;">${msg.content}</span>
                </div>
            `;
        });
    } else {
        showSystemMessage("Error: " + data.error);
    }
}

async function sendMessage() {
    const token = localStorage.getItem('ghostnet_token');
    const content = document.getElementById('message-content').value;
    const ttl = document.getElementById('message-ttl').value;
    // Grab the currently selected cell from the dropdown
    const activeCell = document.getElementById('cell-selector').value;

    if (!content) {
        showSystemMessage("Cannot send an empty message.");
        return;
    }

    const response = await fetch(`${API_BASE}/messages/send`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            cell_id: activeCell, // Send to the active cell!
            content: content,
            ttl: parseInt(ttl) 
        })
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById('message-content').value = ''; 
        fetchMessages(); 
    } else {
        showSystemMessage("Error: " + data.error);
    }
}