from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'betfree-secret-key-troque-em-producao'

DB_PATH = 'betfree.db'

# ─── Banco de dados ───────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    UNIQUE NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reset_tokens (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            email      TEXT NOT NULL,
            token      TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used       INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# ─── Rotas ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id']  = user['id']
            session['username'] = user['username']
            flash('Bem-vindo de volta, ' + user['username'] + '!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha incorretos.', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')
        terms    = request.form.get('terms')

        if not username or not email or not password:
            flash('Preencha todos os campos.', 'error')
        elif len(username) < 3:
            flash('Nome de usuário deve ter pelo menos 3 caracteres.', 'error')
        elif password != confirm:
            flash('As senhas não coincidem.', 'error')
        elif len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'error')
        elif not terms:
            flash('Você precisa aceitar os termos de uso.', 'error')
        else:
            try:
                conn = get_db()
                conn.execute(
                    'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                    (username, email, generate_password_hash(password))
                )
                conn.commit()
                conn.close()
                flash('Conta criada com sucesso! Faça seu login.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('E-mail ou nome de usuário já cadastrado.', 'error')

    return render_template('signup.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    reset_link = None

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        conn  = get_db()
        user  = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:
            # Invalida tokens anteriores do mesmo e-mail
            conn.execute('UPDATE reset_tokens SET used = 1 WHERE email = ?', (email,))
            token      = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=1)
            conn.execute(
                'INSERT INTO reset_tokens (email, token, expires_at) VALUES (?, ?, ?)',
                (email, token, expires_at)
            )
            conn.commit()
            # Em produção: enviar por e-mail. Aqui exibimos na tela (modo dev).
            reset_link = url_for('reset_password', token=token, _external=True)

        conn.close()
        flash('Se o e-mail estiver cadastrado, o link de redefinição aparecerá abaixo.', 'info')
        return render_template('forgot_password.html', reset_link=reset_link)

    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn   = get_db()
    record = conn.execute(
        'SELECT * FROM reset_tokens WHERE token = ? AND used = 0 AND expires_at > ?',
        (token, datetime.now())
    ).fetchone()

    if not record:
        conn.close()
        flash('Link inválido ou expirado. Solicite um novo.', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if password != confirm:
            flash('As senhas não coincidem.', 'error')
        elif len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'error')
        else:
            conn.execute(
                'UPDATE users SET password_hash = ? WHERE email = ?',
                (generate_password_hash(password), record['email'])
            )
            conn.execute('UPDATE reset_tokens SET used = 1 WHERE token = ?', (token,))
            conn.commit()
            conn.close()
            flash('Senha redefinida com sucesso! Faça seu login.', 'success')
            return redirect(url_for('login'))

    conn.close()
    return render_template('reset_password.html', token=token)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Faça login para continuar.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('username'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))


# ─── Inicialização ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
