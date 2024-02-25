from app import *
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


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
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        user_data = cursor.fetchone()
        connection.close()
        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def find_by_email(email):
        connection = sqlite3.connect('Data/Banco.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        user_data = cursor.fetchone()
        connection.close()
        if user_data:
            return User(*user_data)
        return None

    def verify_password(self, password):
        return check_password_hash(self.password, password)
