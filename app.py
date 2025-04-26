from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Otwieranie sesji użytkownika
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123':
            session['loged'] = True
            session['username'] = username
            return "Zalogowano pomyślnie"
        else:
            "Błąd logowania"
    else:
        # Wyświetl formularz logowania
        return render_template('login.html')

@app.route('/protected')
def protected():
    if 'loged' in session:
        return f"Ta strona jest chroniona. Witaj, {session['username']}"
    else:
        return "Dostęp zabroniony. Zaloguj się"
    
@app.route('/logout')
def logout():
    session.pop('loged', None)
    session.pop('username', None)
    return "Wylogowano"

if __name__ == "__main__":
    app.run(debug=True)
