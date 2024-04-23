import os
import requests
from bs4 import BeautifulSoup
import sqlite3

# Função para conectar ao banco de dados
def conectar_banco():
    # Defina o caminho para a pasta que deve conter o arquivo do banco de dados SQLite
    db_folder = os.path.join(os.path.dirname(__file__), '..','Data')
    

    # Verificar se a pasta existe, se não existir, crie-a
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    # Defina o caminho para o arquivo do banco de dados SQLite dentro da pasta
    db_path = os.path.join(db_folder, 'Banco.db')

    # Conectar ao banco de dados e retornar o objeto de conexão
    return sqlite3.connect(db_path)

def create_new_table(conn):
    # Definindo o comando SQL para criar a nova tabela
    conn = conectar_banco()
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()
    
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
    conn = conectar_banco()
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

            # Verificar se o diretório 'imagens_lojas' existe, e criar se não existir
            imagens_lojas_dir = 'static/imagens_lojas'
            if not os.path.exists(imagens_lojas_dir):
                os.makedirs(imagens_lojas_dir)
                

            # Definir o caminho completo do arquivo de imagem
            image_path = os.path.join(imagens_lojas_dir, image_name)

            # Normalizar o caminho
            image_path = image_path.replace('\\', '/')

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