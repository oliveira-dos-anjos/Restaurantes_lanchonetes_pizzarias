from app import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Processar os dados do formulário de login
        return "Processando dados de login..."

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Processar os dados do formulário de registro
        return redirect(url_for('login'))

    return render_template('register.html')


# Rota para solicitar redefinição de senha
@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        # Verificar se o email está cadastrado no banco de dados (simulado aqui)
        email = request.form['email']
        if email == 'usuario@exemplo.com':
            # Gerar código TOTP
            codigo_totp = pyotp.TOTP(chave_mestra).now()
            
            # Enviar código por email
            enviar_email(email, 'Código de Autenticação', f'Seu código de autenticação é: {codigo_totp}')

            return redirect(url_for('redefinir', email=email))
        else:
            return render_template('recuperar.html', mensagem='Email não cadastrado.')

    return render_template('recuperar.html')

# Rota para redefinir senha com verificação do código de autenticação
@app.route('/redefinir', methods=['GET', 'POST'])
def redefinir():
    if request.method == 'POST':
        email = request.form['email']
        codigo_usuario = request.form['codigo']
        codigo_totp = pyotp.TOTP(chave_mestra).now()
        
        if codigo_totp == codigo_usuario:
            # Processar a redefinição de senha
            return redirect(url_for('login'))
        else:
            return render_template('redefinir.html', email=email, mensagem='Código incorreto.')

    # Se acessado via GET, exibir formulário para inserir código de autenticação
    email = request.args.get('email', '')
    return render_template('redefinir.html', email=email)



if __name__ == "__main__":
    app.run(debug=True)
