from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por seguridad

USERS_FILE = 'users.json'

# Cargar usuarios desde JSON
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

# Guardar usuarios en JSON
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('El usuario ya existe')
            return redirect(url_for('register'))

        users[username] = password
        save_users(users)
        flash('Registro exitoso. Inicia sesión.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
