from fastapi import FastAPI, HTTPException, Query, Depends  # Importa classes e funções necessárias do FastAPI
from fastapi.testclient import TestClient
import logging  # Importa a biblioteca de logging para registrar informações e erros
from utils.browser_automation import get_webdriver  # Importa função de scraping de sites
from utils.web_data_extractor import extract_data_from_page, mapear_topicos, mapear_subopcoes
from utils.donwload_files import download_file
import requests

app = FastAPI()

# Configura o logging para registrar informações e erros
logging.basicConfig(level=logging.INFO)

# Define uma rota GET para obter links do website
@app.get("/topicos/")
async def get_website_links():
    """
    Rota GET para obter links do primeiro nível de um website.

    Returns:
        dict: Um dicionário contendo uma lista de links encontrados.

    Raises:
        HTTPException: Se nenhum conteúdo ou link for encontrado.
    """
    # Faz o scraping do site especificado
    website_content = get_webdriver("http://vitibrasil.cnpuv.embrapa.br/")

    if not website_content:
        # Lança uma exceção HTTP 404 se nenhum conteúdo for encontrado
        raise HTTPException(status_code=404, detail="Nenhum conteúdo encontrado")
    
    links_data_topics = mapear_topicos(website_content)
    return links_data_topics

#TODO Fazer ele me entregar o link do download direta para cada subtópico
@app.get("/subtopicos/")
async def get_subtopics(topics: dict = Depends(get_website_links)):
    dict_final = {}
    for key_topic, value_topic in topics.items():
        dict_final[key_topic] = {}
        response = requests.get(value_topic)

        subtopics = mapear_subopcoes(response.text)
        if subtopics:
            for key_subtopic, value_subtopic in subtopics.items():
                path = requests.get(value_subtopic)
                # Pega o conteúdo da página como texto
                conteudo_pagina = path.text
                link_name = extract_data_from_page(conteudo_pagina)
                dict_final[key_topic][key_subtopic] = link_name
        else:
            link_name = extract_data_from_page(response.text)         
            dict_final[key_topic] = link_name 

    return dict_final
    
@app.get("/downlaod/")
async def download(link: str = Query(..., description="URL do link para o arquivo .CSV")):
    logging.info(f"Recebendo link: {link}")
    name_file = link.split("download/")[-1]
    base_url = "http://vitibrasil.cnpuv.embrapa.br/"  
    save_path = f"../storage/{name_file}"  
    download_file(link, base_url, save_path)

    return {"message": "Arquivo CSV baixado e salvo com sucesso"}