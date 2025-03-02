# app/scrapping.py
import os
import requests
from bs4 import BeautifulSoup
from sqlalchemy import text  
from .extensions import db
from .utils import * 
from .models import * 


# Função para fazer uma busca por lojas na região e salvar no banco
def search_and_save(app, city):
    search_url = f"https://kekanto.com.br/{city}"
    response = requests.get(search_url)

    if response.status_code != 200:
        print(f"Erro ao acessar o site: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='store-card')

    with app.app_context():  # Garantir que a execução esteja dentro do contexto do aplicativo
        for result in search_results:
            store_name = result.find('div', class_='store-card-name').text.strip()
            store_details_span = result.find('div', class_='store-card-details').find('span')
            store_details = store_details_span.text.strip() if store_details_span else 'Não disponível'
            opening_hours = result.find('div', class_='open').text.strip() if result.find('div', class_='open') else 'Não disponível'
            image_link = result.find('img')['src'] if result.find('img') else None
            
            address = None
            contact = None

            # Verifica se a loja já existe no banco antes de inserir
            if not loja_existe(store_name):
                # Normalizar nome para evitar problemas com caracteres especiais
                image_name = f"{store_name.replace(' ', '_').replace('/', '')}.png"

                # Configurar a pasta de upload
                imagens_lojas_dir = configure_upload_folder(app, 'imagens')

                # Definir o caminho completo do arquivo de imagem
                image_path = os.path.join(imagens_lojas_dir, image_name)

                # Normalizar o caminho
                image_path = image_path.replace('\\', '/')

                if image_link:
                    # Baixar e salvar a imagem
                    with open(image_path, 'wb') as f:
                        f.write(requests.get(image_link).content)

                # Inserir a nova loja no banco de dados
                insert_data(store_name, store_details, opening_hours, address, contact, image_path)