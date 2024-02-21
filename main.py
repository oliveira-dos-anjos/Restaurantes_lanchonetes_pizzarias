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

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        return redirect(url_for('redefinir'))

    return render_template('recuperar.html')

@app.route('/redefinir', methods=['GET', 'POST'])
def redefinir():
    if request.method == 'POST':
        # Processar os dados do formulário de redefinição de senha
        return redirect(url_for('login'))

    return render_template('redefinir.html')

if __name__ == "__main__":
    app.run(debug=True)
