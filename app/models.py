from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(86), unique=True, nullable=False)
    email = db.Column(db.String(84), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__ (self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
