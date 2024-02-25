import os
#import pyotp
import sqlite3
from app import *
from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Defina o caminho para o arquivo do banco de dados SQLite
db_path = os.path.join(os.path.dirname(__file__), 'Data', 'Banco.db')

# Função para conectar ao banco de dados SQLite
def conectar_banco():
    conn = sqlite3.connect(db_path)
    return conn

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



criar_tabelas()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Processar os dados do formulário de login
        return "Processando dados de login..."

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Verificar se o usuário já existe no banco de dados
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', mensagem='Nome de usuário já cadastrado.')
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', mensagem='Email já cadastrado.')

        if password != confirm_password:
            conn.close()
            return render_template('register.html', mensagem='Senhas não coincidem.')
        
        # Criar um novo usuário
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        conn.close()


        
        return render_template('index.html', mensagem = "Usuário cadastrado com sucesso. Faça login para continuar.")


    return render_template('register.html')


# Rota para solicitar redefinição de senha
@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        try:
            # Verificar se o email está cadastrado no banco de dados
            email = request.form['email']
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                # Gerar e armazenar código OTP na sessão
                codigo_otp = gerar_codigo_otp()
                session['codigo_otp'] = codigo_otp

                # Carregar página de redefinição com o email
                return redirect(url_for('redefinir', email=email))
            else:
                return render_template('recuperar.html', mensagem='Email não cadastrado.')

        except sqlite3.Error as e:
            # Lidar com erros de banco de dados
            return render_template('erro.html', mensagem='Erro no banco de dados: ' + str(e))

    return render_template('recuperar.html')

# Rota para redefinir senha com verificação do código de autenticação
@app.route('/redefinir', methods=['GET', 'POST'])
def redefinir():
    if request.method == 'POST':
        email = request.form['email']
        codigo_usuario = request.form['codigo']
        codigo_otp = session.get('codigo_otp')

        if codigo_usuario == codigo_otp:
            # Redirecionar para a página de redefinição de senha
            return redirect(url_for('login', email=email))
        else:
            return render_template('redefinir.html', email=email, mensagem='Código incorreto.')

    email = request.args.get('email', '')
    codigo = session.get('codigo_otp')  # Obtém o código OTP da sessão
    print("Código OTP:", codigo)  # Aqui você imprime o código na tela
    return render_template('redefinir.html', email=email, codigo=codigo)




if __name__ == "__main__":
    app.run(debug=True)
