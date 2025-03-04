import sqlite3
from app import *
from app.utils import *
from app.models import *
from app.scrapping import *
from urllib.parse import unquote
from flask import send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask import Flask, request, render_template, redirect, url_for, session, flash
from app import create_app

app = create_app()

app.secret_key = 'sua_chave_secreta_aqui'


# Configurar a pasta de upload
upload_folder = configure_upload_folder(app, 'imagens')


with app.app_context():
    search_and_save(app, 'sp/campinas')

original_content = {
    "title": "Locais recentes",
    "content": ""
}

# Configuração da rota para servir imagens da pasta Data
@app.route('/Data/imagens/<filename>')
def serve_data(filename):
    # Caminho absoluto para a pasta Data/imagens
    imagens_dir = os.path.join(app.root_path, '..', 'Data', 'imagens')
    return send_from_directory(imagens_dir, filename)


# Rota para saída de usuário
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


from flask import Flask, render_template, session

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

        # Reverter a ordem da lista de lojas
        lojas_dict_reversed = list(reversed(lojas_dict))  # Ou usar lojas_dict[::-1]

        # Adicionar as lojas ao conteúdo principal
        content_with_lojas = {
            "title": "Locais na região",
            "lojas": lojas_dict_reversed  # Usar a lista revertida
        }

        return render_template("home.html", content=content_with_lojas, user=user)
    
    except Exception as e:
        # Se ocorrer uma exceção ao executar a consulta SQL, renderize uma página em branco
        print(f"Erro: {e}")  # Log do erro para depuração
        return render_template("home.html", content=original_content, user=user)

#Rota para pagina de divulgação
@app.route('/divulgar', methods=['GET', 'POST'])
def divulgar():
    user = session.get('user')

    if request.method == 'POST':
        store_name = request.form.get('store-name')
        closing_time = request.form.get('closing-time')
        min_delivery_time = request.form.get('min-delivery-time')
        max_delivery_time = request.form.get('max-delivery-time')
        address = request.form.get('address')
        contact = request.form.get('phone')
        image_data = request.files.get('preview-image')

        try:
            if loja_existe(store_name):
                return render_template("divulgar.html", user=user, mensagem="Nome de loja já existe.")

            opening_hours = f"Fecha às: {closing_time}" if closing_time else "Não informado"
            store_details = f"Entrega {min_delivery_time} min - {max_delivery_time} min" if min_delivery_time != max_delivery_time else "Entrega : Não informado"

            image_path = None
            if image_data and image_data.filename:
                _, file_extension = os.path.splitext(image_data.filename)
                filename = secure_filename(f"{store_name}{file_extension}")
                save_path = os.path.join(upload_folder, filename)
                
                # Abrir e processar a imagem
                image = Image.open(image_data)
                processed_image = resize_and_crop(image)

                processed_image.save(save_path)  # Salvar imagem tratada
                image_path = f"Data/imagens/{filename}"

            insert_data(store_name, store_details, opening_hours, address, contact, image_path)
            return render_template('divulgar.html', user=user, msg="Loja cadastrada com sucesso!")

        except Exception as e:
            return f"Erro ao cadastrar a loja: {str(e)}", 500

    return render_template("divulgar.html", user=user)



#rota para acessar o perfil da loja
@app.route('/profile', methods=['POST'])
def profile():
    # Recupera a sessão do usuário
    user = session.get('user')

    # Obtém o nome da loja enviado pelo formulário e decodifica
    store_name = unquote(request.form.get('store_name'))

    # Conecta ao banco de dados
    conn = conectar_banco()
    if not conn:
        return "Erro ao conectar ao banco de dados.", 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lojas WHERE store_name = %s', (store_name,))
        store = cursor.fetchone()

        if store:
            store_details = store[2]  # Descrição da loja
            opening_hours = store[3]  # Horário de funcionamento
            image_path = store[6]  # Caminho da imagem

            # Extrair apenas o nome do arquivo do caminho completo
            image_filename = image_path.split('/')[-1]
        else:
            store_details = "Detalhes não encontrados"
            opening_hours = "Horário de funcionamento não encontrado"
            image_filename = "imagem_padrao.png"  # Imagem padrão caso não haja imagem

    except Exception as e:
        return f"Erro ao buscar loja: {e}", 500

    finally:
        cursor.close()
        conn.close()

    return render_template('profile.html',store_name=store_name,store_details=store_details,opening_hours=opening_hours,image_path=image_filename,user=user)

#Rota para area de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_or_username = request.form["email_or_username"]
        password = request.form["password"]

        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            # Verificar se o login é por email ou username
            if "@" in email_or_username:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email_or_username,))
            else:
                cursor.execute("SELECT * FROM users WHERE username = %s", (email_or_username,))

            user = cursor.fetchone()  # Retorna uma tupla com os dados do usuário

            cursor.close()
            conn.close()

            if user:
                user_id, username, email, hashed_password = user[:4]  # Pega os primeiros 4 valores

                if check_password_hash(hashed_password, password):
                    # Autenticação bem-sucedida, armazenar o usuário na sessão
                    session['user'] = {"id": user_id, "username": username, "email": email}
                    flash("Login realizado com sucesso!", "success")
                    return redirect(url_for('home'))  
                else:
                    flash("Senha incorreta!", "danger")
            else:
                flash("Usuário não encontrado!", "danger")

        except Exception as e:
            flash(f"Ocorreu um erro ao processar o login: {str(e)}", "danger")

    return render_template("login.html")



#Rota para registrar novo usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validação básica
        if password != confirm_password:
            flash('Senhas não coincidem.', 'danger')
            return render_template('register.html')

        # Verificar se o usuário já existe
        if User.find_by_username(username) or User.find_by_email(email):
            flash('Nome de usuário ou email já cadastrado.', 'danger')
            return render_template('register.html')

        # Criar novo usuário
        try:
            new_user = User(username=username, email=email, password=password)
            new_user.save()
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'danger')

    return render_template('register.html')


@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email = request.form['email']
        usuario = User.find_by_email(email)  # Busca usuário via SQLAlchemy

        if usuario:
            # Gerar código OTP e armazenar na sessão
            codigo_otp = gerar_codigo_otp()
            session['codigo_otp'] = codigo_otp
            session['email_redefinicao'] = email  # Armazena email na sessão
            enviar_email_otp(email, codigo_otp)

            flash("Código enviado para seu email.", "success")
            return redirect(url_for('redefinir'))

        flash("Email não cadastrado.", "danger")

    return render_template('recuperar.html')

# Rota para redefinir senha com verificação do código de autenticação
@app.route('/redefinir', methods=['GET', 'POST'])
def redefinir():
    email = session.get('email_redefinicao')  # Recupera email armazenado na sessão
    codigo_otp = session.get('codigo_otp')

    if request.method == 'POST':
        codigo_usuario = request.form['codigo']
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirmar_senha']

        if not email or not codigo_otp:
            flash("Sessão expirada. Tente novamente.", "warning")
            return redirect(url_for('recuperar'))

        if codigo_usuario == codigo_otp and nova_senha == confirmar_senha:
            if len(nova_senha) < 6:
                flash("A senha deve ter pelo menos 6 caracteres.", "danger")
                return render_template('redefinir.html', email=email)

            # Atualiza a senha do usuário
            User.new_password(email, nova_senha)

            # Limpa os dados da sessão após a redefinição da senha
            session.pop('codigo_otp', None)
            session.pop('email_redefinicao', None)

            flash("Senha redefinida com sucesso!", "success")
            return redirect(url_for('login'))

        flash("Código incorreto ou senhas não correspondem.", "danger")

    return render_template('redefinir.html', email=email)

#Rota para pesquisa de lojas
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
        cursor.execute("SELECT id FROM lojas WHERE store_name ILIKE %s", (pesquisa,))  # Use %s para PostgreSQL
        ids_lojas = [row[0] for row in cursor.fetchall()]

        if ids_lojas:
            # Consultar todas as informações das lojas correspondentes
            query = "SELECT * FROM lojas WHERE id IN ({})".format(','.join(['%s'] * len(ids_lojas)))
            cursor.execute(query, ids_lojas)
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

    except Exception as e:
        # Se ocorrer uma exceção ao executar a consulta SQL, renderize uma página com mensagem de erro
        print(f"Erro ao buscar lojas: {e}")
        return render_template("home.html", content=original_content, user=user)
 
if __name__ == "__main__":
    app.run(debug=True)
