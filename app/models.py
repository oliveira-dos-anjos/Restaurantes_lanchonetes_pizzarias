import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Função para conectar ao banco de dados SQLite
def conectar_banco():
    db_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data')

    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    db_path = os.path.join(db_folder, 'Banco.db')

    conn = sqlite3.connect(db_path)
    return conn

# Função para criar as tabelas no banco de dados
def create_table():
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

def create_new_table():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lojas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_name TEXT,
        store_details TEXT,
        opening_hours TEXT,
        contact NUMBER,
        address TEXT,
        image_path TEXT
    )
    ''')
    conn.commit()
    conn.close()

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        connection = sqlite3.connect('Data/Banco.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (self.username, self.email, self.password))
        connection.commit()
        connection.close()

    @staticmethod
    def find_by_username(username):
        connection = sqlite3.connect('Data/Banco.db')
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM users WHERE username=?', (username,))
        user_id = cursor.fetchone()
        connection.close()
        if user_id:
            return user_id[0]  # Acessa o primeiro elemento da tupla
        else:
            return None

    @staticmethod
    def find_by_email(email):
        connection = sqlite3.connect('Data/Banco.db')
        cursor = connection.cursor()
        cursor.execute('SELECT email FROM users WHERE email=?', (email,))
        user_id = cursor.fetchone()
        connection.close()
        if user_id:
            return user_id[0]  # Acessa o primeiro elemento da tupla
        else:
            return None



    def verify_password(user, pwd):
        if "@" in user:
            connection = sqlite3.connect('Data/Banco.db')
            cursor = connection.cursor()
            cursor.execute('SELECT password FROM users WHERE email=?', (user,))
            stored_password_hash = cursor.fetchone()
            connection.close()
        else:
            connection = sqlite3.connect('Data/Banco.db')
            cursor = connection.cursor()
            cursor.execute('SELECT password FROM users WHERE username=?', (user,))
            stored_password_hash = cursor.fetchone()
            connection.close()


        if stored_password_hash:
            stored_password_hash = stored_password_hash[0]
            # Verificando se a senha fornecida corresponde ao hash da senha armazenada
            return check_password_hash(stored_password_hash, pwd)
        else:
            return False

    def new_password(email, nova_senha):
        connection = None 
        try:
            connection = sqlite3.connect('Data/Banco.db')
            cursor = connection.cursor()

            # Verificar se o email existe na tabela
            cursor.execute('SELECT email FROM users WHERE email=?', (email,))
            user = cursor.fetchone()
            if user:
                # Se o email existir, atualizar a senha
                hashed_password = generate_password_hash(nova_senha)
                cursor.execute('UPDATE users SET password=? WHERE email=?', (hashed_password, email))
                connection.commit()

        except sqlite3.Error as error:
            return f"Erro ao atualizar a senha:", error

create_new_table()
create_table()
