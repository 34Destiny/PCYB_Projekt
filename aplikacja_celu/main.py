from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin"
SESSION_COOKIE_NAME = "PCYB_forum_session"
SESSION_COOKIE_VALUE = "admin_session_token_pcyb"

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            response = make_response(redirect('/protected'))
            response.set_cookie(SESSION_COOKIE_NAME, SESSION_COOKIE_VALUE, httponly=False, secure=False, samesite='Lax')
            return response
        else:
            error = "Niepoprawna nazwa użytkownika lub hasło."

    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if session_cookie == SESSION_COOKIE_VALUE:
        return redirect('/protected')
    return render_template('login.html', error=error)

@app.route('/protected')
def protected():
    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if session_cookie == SESSION_COOKIE_VALUE:
        return render_template('protected.html', session_cookie=f"{SESSION_COOKIE_NAME}={session_cookie}")
    return redirect('/')

@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
