# PCYB Cybersecurity Project - Session Hijacking Demo

Projekt demonstracyjny pokazujący podatności session hijacking w aplikacji webowej.

## 🚀 Szybki start

### 1. Uruchom aplikację celu (Docker)
```powershell
cd aplikacja_celu
docker-compose up -d --build
```

Aplikacja będzie dostępna pod: http://localhost:5000
- Login: `admin`
- Hasło: `admin`

### 2. Zainstaluj zależności dla payloadu
```powershell
cd payload
pip install -r requirements.txt
```

### 3. Uruchom exploit
```powershell
python session_hijack.py
```

## 📂 Struktura projektu

```
PCYB_Projekt/
│
├── aplikacja_celu/              # Aplikacja podatna (target)
│   ├── main.py                  # Flask app z podatnościami
│   ├── templates/               # Szablony HTML
│   ├── static/                  # CSS, statyczne pliki
│   ├── Dockerfile               # Kontener dla aplikacji
│   ├── docker-compose.yml       # Compose configuration
│   ├── requirements.txt         # Zależności Python
│   └── README_DOCKER.md         # Dokumentacja Docker
│
└── payload/                     # Exploit/payload
    ├── session_hijack.py        # Skrypt demonstrujący atak
    ├── requirements.txt         # Zależności dla exploita
    └── README.md                # Szczegółowa dokumentacja

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
    samesite='Lax'     # ⚠️  Zbyt permisywne
)
```

### 3. Brak walidacji sesji
- Brak timeout sesji
- Brak powiązania z IP
- Brak regeneracji tokena
- Brak ochrony CSRF

## 🔍 Demonstrowane wektory ataku

1. **Atak na przewidywalny token** - bezpośrednie wstrzyknięcie znanego tokena
2. **Kradzież cookie przez XSS** - symulacja wycieku przez JavaScript
3. **Replay attack** - powtórzenie przechwyconej sesji
4. **Ekstrakcja informacji** - analiza właściwości cookie

## 📊 Przykładowy output

```
============================================================
ATTACK VECTOR #1: Predictable Session Token
============================================================
[✓] SESSION HIJACK SUCCESSFUL!
[✓] Gained unauthorized access to protected page
```

## 🛡️ Zalecenia bezpieczeństwa

**Co należy naprawić:**
- ✓ Użyć kryptograficznie bezpiecznych tokenów (`secrets.token_urlsafe()`)
- ✓ Ustawić `httponly=True` (ochrona przed XSS)
- ✓ Ustawić `secure=True` (tylko HTTPS)
- ✓ Dodać timeout sesji
- ✓ Implementować walidację sesji (IP, User-Agent)
- ✓ Użyć `samesite='Strict'`
- ✓ Dodać tokeny CSRF
- ✓ Logować podejrzane aktywności

## 📝 Do raportu

Należy opisać:
1. **Zidentyfikowane podatności** - lista z kodami CWE
2. **Metoda eksploatacji** - jak działa atak
3. **Ocena wpływu** - co atakujący może zrobić
4. **Proof of Concept** - screenshoty/logi ze skryptu
5. **Rekomendacje** - konkretne poprawki
6. **Weryfikacja** - jak sprawdzić, że poprawka działa

## ⚠️ Disclaimer

Ten projekt jest stworzony wyłącznie w celach edukacyjnych w ramach zajęć z cyberbezpieczeństwa. 
Aplikacja celowo zawiera podatności do nauki.

**NIGDY** nie używaj tych technik na systemach, do których nie masz wyraźnego pozwolenia!

---

**Projekt:** PCYB  
**Data:** Październik 2025
