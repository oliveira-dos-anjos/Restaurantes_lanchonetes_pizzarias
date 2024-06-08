import os
import sqlite3
from app.models import *
from app import *
from werkzeug.security import generate_password_hash
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


original_content = {
    "title": "Locais recentes",
    "content": "Aqui estão os resultados da sua pesquisa:"
}


criar_tabelas()

# Rota para saída de usuário
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# Rota para tela inicial
@app.route("/")
def home():
    # Recuperar o usuário da sessão
    user = session.get('user')
    
    try:
        # Conectar ao banco de dados
        conn = conectar_banco()
        cursor = conn.cursor()

        # Consultar os dados das lojas
        cursor.execute("SELECT * FROM lojas")
        lojas = cursor.fetchall()
        
        # Fechar a conexão com o banco de dados
        conn.close()

        # Converter os resultados da consulta em um dicionário
        lojas_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in lojas]

        # Substituir as contra barras nos caminhos das imagens
        for loja in lojas_dict:
            if 'image_path' in loja:
                loja['image_path'] = loja['image_path'].replace('\\', '/')
                loja['image_path'] = loja['image_path'].replace('static', '')


        # Adicionar as lojas ao conteúdo principal
        content_with_lojas = {
            "title": "Locais na região",
            "lojas": lojas_dict
        }

        return render_template("home.html", content=content_with_lojas, user=user)
    except sqlite3.Error as e:
        # Se ocorrer uma exceção ao executar a consulta SQL, renderize uma página em branco
        return render_template("home.html", content=original_content, user=user)


#rota para acessar o perfil da loja
@app.route('/profile', methods=['POST'])
def profile():
    # recupera a sessão do usuario
    user = session.get('user')

    store_name = request.form.get('store_name')
    store_details = request.form.get('store_details')
    opening_hours = request.form.get('opening_hours')
    image_path = request.form.get('image_path')
    print(f"\033[31m{image_path}")

    # Agora você pode usar esses dados no seu template ou processamento adicional
    return render_template('profile.html', store_name=store_name, store_details=store_details, opening_hours=opening_hours, image_path=image_path, user=user)


#Rota para area de login
@app.route("/login", methods=["GET", "POST"])
def login():
    mensagem = None 

    if request.method == "POST":
        email_or_username = request.form["email_or_username"]
        password = request.form["password"]

        try:
            # Verificar se o login é um email ou um username
            if "@" in email_or_username:
                user = User.find_by_email(email_or_username)
            else:
                user = User.find_by_username(email_or_username)

            if user:
                if User.verify_password(user, password):

                    # Autenticação bem-sucedida, armazenar o usuário na sessão
                    session['user'] = user
                    return redirect(url_for('home')) 
                else:
                    mensagem = "Senha incorreta!"
            else:
                mensagem = "Usuário não encontrado!"
        except Exception as e:
            mensagem = f"Ocorreu um erro ao processar o login: {str(e)}"

    # Passar a mensagem para o template e renderizar o template
    return render_template("login.html", mensagem=mensagem)

#Rota para registrar novo usuario
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
       

        
        return render_template('login.html',  msg= "Faça login para continuar.")


    return render_template('register.html')

# Rota para solicitar redefinição de senha
@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        try:
            # Verificar se o email está cadastrado no banco de dados
            email = request.form['email']
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                # Gerar e armazenar código OTP na sessão
                codigo_otp = gerar_codigo_otp()
                session['codigo_otp'] = codigo_otp
                enviar_email_otp(email, codigo_otp)

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
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirmar_senha']
        codigo_otp = session.get('codigo_otp')

        if codigo_usuario == codigo_otp and nova_senha == confirmar_senha:
            # Redefinir a senha do usuário
            User.new_password(email, nova_senha)

            # Limpar o código OTP da sessão após a redefinição da senha
            session.pop('codigo_otp', None)

            return redirect(url_for('login'))

        else:
            return render_template('redefinir.html', email=email, mensagem='Código incorreto ou senhas não correspondem.')

    email = request.args.get('email', '')
    codigo = session.get('codigo_otp')
    print("Código OTP:", codigo)  # Aqui você imprime o código na tela
    return render_template('redefinir.html', email=email, codigo=codigo)

@app.route("/search", methods=["GET"])
def search():
    
    # Recuperar o usuário da sessão
    user = session.get('user')

    resultados = ["resultado1", "resultado2", "resultado3"]

    # Obter o termo de pesquisa da query string
    termo_pesquisa = request.args.get("q", "")

    # Realizar a lógica de pesquisa aqui (pode ser uma busca em um banco de dados, por exemplo)
    # Neste exemplo, vamos apenas verificar se há um termo de pesquisa e retornar um resultado simulado
    if termo_pesquisa:

        # Se houver um termo de pesquisa, renderizar o template com os resultados
        resultados = {"title": f"Resultados da Pesquisa para: {termo_pesquisa}", "content": "Aqui estão os resultados da pesquisa..."}
        return render_template("home.html", content=resultados, user=user)
    else:
        # Se nenhum termo de pesquisa for fornecido, renderizar o template com o conteúdo original da página
        return render_template("home.html", content=original_content, user=user)
    

if __name__ == "__main__":
    app.run(debug=True)
