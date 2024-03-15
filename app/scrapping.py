from bs4 import BeautifulSoup
import requests


def google_search(query, city):
    search_url = f"https://www.google.com/search?q={query}+{city}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='g')
    
    # Extrair informações desejadas, como títulos e links para imagens
    result_data = []
    for result in search_results:
        title = result.h3.text if result.h3 else None
        image_link = result.find('img')['src'] if result.find('img') else None
        result_data.append({'title': title, 'image_link': image_link})
    
    return result_data

# Lista de termos de pesquisa
Lista_de_pesquisa = ['pizzaria', 'restaurantes', 'bares', 'pub', 'balada']
cidade = ['campinas-sp', 'campinas-sp', 'campinas-sp', 'campinas-sp', 'campinas-sp']

# Percorrer a lista de termos de pesquisa e adicionar os resultados à lista principal
search_results_list = []
for term, city in zip(Lista_de_pesquisa, cidade * len(Lista_de_pesquisa)):
    results = google_search(term, city)
    search_results_list.append(results)

# Exibir os resultados da pesquisa para cada termo
for index, term_results in enumerate(search_results_list, 1):
    print(f"Resultados para o termo {Lista_de_pesquisa[index-1]} na cidade {cidade[index-1]}:")
    for result in term_results:
        print(f"Title: {result['title']}")
        print(f"Image Link: {result['image_link']}")
        print()
