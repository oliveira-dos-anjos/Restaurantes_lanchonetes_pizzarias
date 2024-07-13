import os
import requests
from app import *
from app.models import *
from bs4 import BeautifulSoup

    
def insert_data(conn, store_name, store_details, opening_hours, address, contact,image_path):
    # Definindo o comando SQL para inserir os dados na tabela
    insert_query = '''
    INSERT INTO lojas (store_name, store_details, opening_hours, address, contact,image_path)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    # Executando o comando SQL para inserir os dados na tabela
    conn.execute(insert_query, (store_name, store_details, opening_hours, address, contact,image_path))
    # Comitando as mudanças
    conn.commit()

#Função para verificar se a loja existe no banco
def loja_existe(conn, store_name):
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM lojas WHERE store_name = ?', (store_name,))
    return cursor.fetchone() is not None


def search_and_save(city):
    search_url = f"https://kekanto.com.br/{city}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='store-card')
    
    # Conectar ao banco de dados existente
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Extrair informações desejadas e salvar na nova tabela
    for result in search_results:
        store_name = result.find('div', class_='store-card-name').text.strip()
        store_details_span = result.find('div', class_='store-card-details').find('span')
        store_details = store_details_span.text.strip() if store_details_span else 'Não disponível'
        opening_hours = result.find('div', class_='open').text.strip() if result.find('div', class_='open') else 'Não disponível'
        image_link = result.find('img')['src'] if result.find('img') else None
        
        address = None
        contact = None
        
        # Verificar se a loja já existe no banco de dados
        if not loja_existe(conn, store_name):

            # Salva as imagens
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
            insert_data(conn, store_name, store_details, opening_hours, address, contact,image_path)
        
    # Fechar a conexão com o banco de dados
    conn.close()

# Exemplo de uso:
search_and_save('sp/campinas')