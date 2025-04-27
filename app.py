import sqlite3
from flask import Flask, render_template, request, session, g

DATABASE = 'portal.db' # Database filename
app = Flask(__name__)
app.secret_key = "secret_key"

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


#dodawanie faktur kosztowych

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'logged_in' in session:
        db = get_db()
        cursor = db.cursor()

        if request.method == 'POST':
            description = request.form['description']
            amount_net = request.form['amount_net']
            amount_gross = request.form['amount_gross']
            vat_value = request.form['vat_value']
            date = request.form.get['date']
            driver_id = request.form.get('driver_id')

            if session['role'] == 'administrator':
                cursor.execute("INSERT INTO expenses (user_id, driver_id, date, description, amount_net, amount_gross, vat_value) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (session['user_id'], driver_id if driver_id else None, date, description, amount_net, amount_gross, vat_value))
            elif session['role'] == 'driver':
                cursor.execute("SELECT id FROM drivers WHERE user_id = ?", (session['user_id'],))
                driver = cursor.fetchone()
                if driver:
                    cursor.execute("INSERT INTO expenses (user_id, driver_id, date, description, amount_net, amount_gross, vat_value) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                   (session['user_id'], driver['id'], date, description, amount_net, amount_gross, vat_value))
                else:
                    return "Błąd. Nie znaleziono danych kierowcy dla tego użytkownika"
            db.commit()
            return "Faktura dodana pomyślnie"
        else:
            drivers = []
            if session['role'] == 'administrator':
                cursor.execute("SELECT id, first_name, last_name FROM drivers")
                drivers = cursor.fetchall()
            return render_template('add_expense.html', drivers=drivers)
    else:
        return "wymagane logowanie"

# panel admin z listą kierowców
@app.route('/admin/drivers')
def admin_drivers():
    if 'logged_in' in session and session['role'] == 'administrator':
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT d.id, d.first_name, d.last_name, u.username FROM drivers d JOIN users u ON d.user_id = u.id")
        drivers = cursor.fetchall()
        return render_template('admin/drivers.html', drivers=drivers)
    else:
        return "Dostęp tylko dla administratora"


# do usunięcia wkrótce - tylko na testy
users = {
    'admin': {'password': 'admin123', 'role': 'administrator'},
    'driver1': {'password': 'driver1password', 'role': 'driver'},
    'driver2': {'password': 'driver2password', 'role': 'driver'}
}


# logowanie do portalu
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

#panel administratora
@app.route('/admin')
def admin_panel():
    if 'logged_in' in session and session['role'] == 'administrator':
        return f"Panel administratora. {session['username']}"
    else:
        return "Dostęp tylko dla administratora"

#panel kierowcy
@app.route('/driver')
def driver_panel():
    if 'logged_in' in session and session['role'] == 'driver':
        return f"Panel kierowcy, {session['username']}"
    else:
        return "Dostęp tylko dla zalogowanego kierowcy"


#wylogowywanie się z portalu
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None)
    return "Wylogowano"

if __name__ == "__main__":
    # init_db() #inicjalizacja bazy danych przy pierwszym uruchomieniu
    app.run(debug=True)