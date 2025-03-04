from .utils import conectar_banco
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db 
from sqlalchemy import text  
from sqlalchemy.exc import IntegrityError
# Classe de modelo User para a tabela 'users'
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    @staticmethod
    def new_password(email, nova_senha):
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(nova_senha)
            db.session.commit()
            return True
        return False

# Classe de modelo Loja para a tabela 'lojas'
class Loja(db.Model):
    __tablename__ = 'lojas'

    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(100), unique=True, nullable=False)
    store_details = db.Column(db.String(200))
    opening_hours = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    address = db.Column(db.String(200))
    image_path = db.Column(db.String(200))

    def __repr__(self):
        return f"<Loja {self.store_name}>"
    
# Função para verificar se a loja existe no banco (usando SQLAlchemy)
def loja_existe(store_name):
    with db.engine.connect() as conn:
        # Usar a função text para criar uma consulta executável
        query = text("SELECT 1 FROM lojas WHERE store_name = :store_name")
        result = conn.execute(query, {"store_name": store_name})
        return result.fetchone() is not None

# Função para inserir dados de scrapping ao banco
def insert_data(store_name, store_details, opening_hours, address, contact, image_path):
    # Verifica se a loja já existe no banco de dados
    if loja_existe(store_name):
        return  # Sai da função sem inserir

    # Cria um novo registro
    new_store = Loja(
        store_name=store_name,
        store_details=store_details,
        opening_hours=opening_hours,
        address=address,
        contact=contact,
        image_path=image_path
    )

    try:
        db.session.add(new_store)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Desfaz a transação em caso de erro

def insert_store(store_name, store_details, opening_hours, address, contact, image_path):
    try:
        conn = conectar_banco()
        shift_ids(conn)

        # Inserir a nova loja no ID 1
        new_store = Loja(
            id = 01
            store_name=store_name,
            store_details=store_details,
            opening_hours=opening_hours,
            address=address,
            contact=contact,
            image_path=image_path
        )
        db.session.add(new_store)
        db.session.commit()

    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        raise  # Re-lança a exceção para ser tratada na rota


# Função para mover os IDs da tabela 'lojas'
def shift_ids(conn):
    cursor = conn.cursor()

    try:
        # Selecionar todos os IDs em ordem decrescente
        cursor.execute("SELECT id FROM lojas ORDER BY id DESC")
        ids = cursor.fetchall()

        # Atualizar os IDs em ordem decrescente para evitar conflitos
        for id_tuple in ids:
            cursor.execute("UPDATE lojas SET id = id + 1 WHERE id = %s", (id_tuple[0],))
            conn.commit()

        print("IDs atualizados com sucesso.")
    except Exception as e:
        conn.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao atualizar IDs: {e}")
        raise  # Re-lança a exceção para ser tratada na função que chamou shift_ids
    finally:
        cursor.close()