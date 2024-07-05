import sqlite3
from app.models import *
from app import *
from werkzeug.security import generate_password_hash
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

original_content = {
    "title": "Locais recentes",
    "content": ""
}

create_table()

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

#Rota para pagina de divulgação
@app.route('/divulgar', methods=['GET', 'POST'])
def divulgar():
    # Recuperar usuário da sessão (se necessário)
    user = session.get('user')
    
    if request.method == 'POST':
        # Recuperar a imagem enviada
        image = request.files.get('image-src')
        store_name = request.form.get('store-name')
        opening_time = request.form.get('opening-time')
        closing_time = request.form.get('closing-time')
        min_delivery_time = request.form.get('min-delivery-time')
        max_delivery_time = request.form.get('max-delivery-time')
        address = request.form.get('address')
        phone = request.form.get('phone')

        # Verifica e cria o diretório para salvar a imagem
        save_dir = 'static/imagens_lojas'  # Defina seu diretório de salvamento aqui

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Salva a imagem se ela for enviada
        if image:
            image_path = os.path.join(save_dir, image.filename)
            image.save(image_path)
            print(f"Imagem salva em: {image_path}")


        # Exibe os dados no terminal para depuração
        print(f"\033[31mImagem da Loja: {image}\nLoja: {store_name}\nHorário de Abertura: {opening_time}\nHorário de Fechamento: {closing_time}\nTempo Mínimo de Entrega: {min_delivery_time}\nTempo Máximo de Entrega: {max_delivery_time}\nEndereço: {address}\nTelefone: {phone}\033[0m")
    
    return render_template("divulgar.html", user=user)

#rota para acessar o perfil da loja
@app.route('/profile', methods=['POST'])
def profile():
    # recupera a sessão do usuario
    user = session.get('user')

    store_name = request.form.get('store_name')
    store_details = request.form.get('store_details')
    opening_hours = request.form.get('opening_hours')
    image_path = request.form.get('image_path')

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
    print("Código OTP:", codigo)
    return render_template('redefinir.html', email=email, codigo=codigo)

@app.route("/search", methods=["GET"])
def search():
    try:
        # Conectando ao banco
        conn = conectar_banco()
        cursor = conn.cursor()

        # Recuperar o usuário da sessão
        user = session.get('user')

        # Obter o termo de pesquisa da query string
        termo_pesquisa = request.args.get("q", "")

        # Verificar se há lojas correspondentes com a pesquisa no banco
        pesquisa = f"%{termo_pesquisa}%"
        cursor.execute('SELECT id FROM lojas WHERE store_name LIKE ?', (pesquisa,))
        ids_lojas = [row[0] for row in cursor.fetchall()]

        if ids_lojas:
            # Consultar todas as informações das lojas correspondentes
            cursor.execute('SELECT * FROM lojas WHERE id IN ({})'.format(','.join('?' for _ in ids_lojas)), ids_lojas)
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
                "title": f"Resultados da Pesquisa para: {termo_pesquisa}",
                "lojas": lojas_dict
            }

            return render_template("home.html", content=content_with_lojas, user=user)
        
        else:
            return render_template("home.html", content=original_content, user=user)   

    except sqlite3.Error as e:
        # Se ocorrer uma exceção ao executar a consulta SQL, renderize uma página com mensagem de erro
        return render_template("home.html", content=original_content, user=user)
 
if __name__ == "__main__":
    app.run(debug=True)
