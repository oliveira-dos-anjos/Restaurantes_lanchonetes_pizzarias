import os
import requests
from bs4 import BeautifulSoup
import sqlite3

def create_new_table(conn):
    # Definindo o comando SQL para criar a nova tabela
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS lojas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_name TEXT,
        store_details TEXT,
        opening_hours TEXT,
        image_path TEXT
    )
    '''
    # Executando o comando SQL para criar a nova tabela
    conn.execute(create_table_query)

def insert_data(conn, store_name, store_details, opening_hours, image_path):
    # Definindo o comando SQL para inserir os dados na tabela
    insert_query = '''
    INSERT INTO lojas (store_name, store_details, opening_hours, image_path)
    VALUES (?, ?, ?, ?)
    '''
    # Executando o comando SQL para inserir os dados na tabela
    conn.execute(insert_query, (store_name, store_details, opening_hours, image_path))
    # Comitando as mudanças
    conn.commit()

def search_and_save(city):
    search_url = f"https://kekanto.com.br/{city}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='store-card')
    
    # Conectar ao banco de dados existente
    db_path = os.path.join(os.path.dirname(__file__), 'Data', 'Banco.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criar a nova tabela se ainda não existir
    create_new_table(conn)
    
    # Extrair informações desejadas e salvar na nova tabela
    for result in search_results:
        store_name = result.find('div', class_='store-card-name').text.strip()
        store_details_span = result.find('div', class_='store-card-details').find('span')
        store_details = store_details_span.text.strip() if store_details_span else None
        opening_hours = result.find('div', class_='open').text.strip() if result.find('div', class_='open') else None
        image_link = result.find('img')['src'] if result.find('img') else None
        
        # Salvar a imagem na pasta 'static/imagens_lojas'
        if image_link:
            image_name = f"{store_name.replace(' ', '_')}.png"
            image_path = os.path.join('static/imagens_lojas', image_name)
            with open(image_path, 'wb') as f:
                f.write(requests.get(image_link).content)
        else:
            image_path = None
        
        # Inserir os dados na nova tabela
        insert_data(conn, store_name, store_details, opening_hours, image_path)
    
    # Fechar a conexão com o banco de dados
    conn.close()

# Exemplo de uso:
search_and_save('sp/campinas')
