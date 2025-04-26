from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "secret_key"

users = {
    'admin': {'password': '123', 'role': 'administrator'},
    'driver': {'password': '321', 'role': 'driver'}
}

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Otwieranie sesji użytkownika
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = users[username]['role']
            return f"Zalogowano jako {session['role']}!"
        else:
            "Błąd logowania"
    else:
        # Wyświetl formularz logowania
        return render_template('login.html')

@app.route('/admin')
def admin_panel():
    if 'logged_in' in session and session['role'] == 'administrator':
        return f"Panel administratora. {session['username']}"
    else:
        return "Dostęp tylko dla administratora"
    
@app.route('/driver')
def driver_panel():
    if 'logged_in' in session and session['role'] == 'driver':
        return f"Panel kierowcy, {session['username']}"
    else:
        return "Dostęp tylko dla zalogowanego kierowcy"
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None)
    return "Wylogowano"

if __name__ == "__main__":
    app.run(debug=True)
