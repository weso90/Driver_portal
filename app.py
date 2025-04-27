import sqlite3
from flask import Flask, render_template, request, session, g

DATABASE = 'portal.db' # Nazwa pliku bazy danych

app = Flask(__name__)
app.secret_key = "secret_key"

users = {
    'admin': {'password': '123', 'role': 'administrator'},
    'driver': {'password': '321', 'role': 'driver'}
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # pozwala na dostęp do kolumn po nazwach
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == "__main__":
    init_db() # Inicjalizuj bazę danych przy pierwszym uruchomieniu
    app.run(debug=True)

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