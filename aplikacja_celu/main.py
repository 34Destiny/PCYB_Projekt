from flask import Flask, request, make_response, redirect, render_template
from datetime import datetime

app = Flask(__name__)

USERS = {
    "admin": {"password": "admin", "session_token": "admin_session_token_pcyb"},
    "user": {"password": "user", "session_token": "user_session_token_pcyb"}
}

SESSION_COOKIE_NAME = "PCYB_forum_session"

posts = []

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS and USERS[username]['password'] == password:
            response = make_response(redirect('/protected'))
            session_token = USERS[username]['session_token']
            response.set_cookie(SESSION_COOKIE_NAME, session_token, httponly=False, secure=False, samesite='Lax')
            return response
        else:
            error = "Niepoprawna nazwa użytkownika lub hasło."

    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if session_cookie:
        for username, user_data in USERS.items():
            if user_data['session_token'] == session_cookie:
                return redirect('/protected')
    return render_template('login.html', error=error)

@app.route('/protected')
def protected():
    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    current_user = None
    
    if session_cookie:
        for username, user_data in USERS.items():
            if user_data['session_token'] == session_cookie:
                current_user = username
                break
    
    if current_user:
        search_query = request.args.get('search', '')
        
        return render_template('protected.html', 
                             username=current_user, 
                             posts=reversed(posts),
                             session_cookie=f"{SESSION_COOKIE_NAME}={session_cookie}",
                             search_query=search_query)
    return redirect('/')

@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response

@app.route('/add_post', methods=['POST'])
def add_post():
    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    current_user = None
    
    if session_cookie:
        for username, user_data in USERS.items():
            if user_data['session_token'] == session_cookie:
                current_user = username
                break
    
    if current_user:
        post_content = request.form.get('content', '').strip()
        if post_content:
            post = {
                'id': len(posts) + 1,
                'author': current_user,
                'content': post_content,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            posts.append(post)
    
    return redirect('/protected')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
