from src.utils.web_data_extractor import extract_data_from_page, mapear_topicos, mapear_subopcoes
from src.auth.auth_handler import sign_jwt
from src.auth.auth_bearer import JWTBearer
from src.utils.model import PostSchema, UserSchema, UserLoginSchema
from src.auth.check_users import check_user 
from src.utils.browser_automation import get_webdriver  # Importa função de scraping de sites
from src.utils.download_files import download_file
from src.utils.show_info import load_csv_with_separator
from fastapi import FastAPI, HTTPException, Query, Depends, Body  # Importa classes e funções necessárias do FastAPI
from fastapi.responses import HTMLResponse
from typing import List, Optional
from tabulate import tabulate
import logging 
import requests

app = FastAPI()

# Configura o logging para registrar informações e erros
logging.basicConfig(level=logging.INFO)

# Define uma rota GET para obter links do website
@app.get("/topicos/", dependencies=[Depends(JWTBearer())])
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
    """
    Processa um dicionário de tópicos para extrair links de subopções e páginas associadas.

    Para cada tópico, faz uma requisição HTTP para obter subopções. Para cada subopção, extrai os links de uma página. 
    Se não houver subopções, extrai os links diretamente da página do tópico.

    Args:
        topics (dict): Dicionário com tópicos e URLs associados.

    Returns:
        dict: Dicionário com tópicos e subopções, incluindo os links extraídos.
    """
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
    
@app.get("/download/")
async def download_f(name_file: str = Query(..., description="Nome do arquivo .CSV")):
    """
    Faz o download de um arquivo CSV e o salva no diretório especificado.

    Recebe o nome de um arquivo CSV, constrói o URL para download e salva o arquivo no diretório `../storage`.

    Args:
        name_file (str): Nome do arquivo CSV a ser baixado.

    Returns:
        dict: Mensagem de sucesso se o arquivo for baixado e salvo com sucesso.

    Raises:
        HTTPException: Se ocorrer um erro durante o download.
    """
    try:
        logging.info(f"Recebendo link: {name_file}")
        base_url = "http://vitibrasil.cnpuv.embrapa.br/download/"
        save_path = f"../storage/{name_file}"
        download_file(name_file, base_url, save_path)
        
        return {"message": "Arquivo CSV baixado e salvo com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao baixar o arquivo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao baixar o arquivo")

@app.get("/show/", response_class=HTMLResponse)
async def show(
    link: str = Query(..., description="Nome do arquivo .CSV"),
    anos: str = Query(None, description="Coloque os anos a serem filtrados, separados por vírgulas (ex: 1970,1971,1980).")
):
    """
    Exibe uma tabela HTML com dados filtrados de um arquivo CSV.

    Recebe o nome do arquivo CSV e opcionalmente anos para filtragem. Carrega o arquivo, filtra por anos se fornecidos, 
    e retorna uma tabela HTML com os dados filtrados.

    Args:
        link (str): Nome do arquivo CSV a ser carregado.
        anos (str, optional): Anos a serem filtrados, separados por vírgulas.

    Returns:
        HTMLResponse: Tabela HTML com os dados filtrados ou mensagem de erro.

    Raises:
        HTTPException: Se ocorrer um erro inesperado.
    """
    try:
        logging.info(f"Recebendo nome: {link}")
        name_file = link.split("download/")[-1]
        save_path = f"./src/storage/{name_file}"  

        logging.info(f"Carregando o arquivo: {save_path}")
        
        # Carregar o arquivo CSV
        df = load_csv_with_separator(save_path, [';', '\t', ','])

        # Identificar colunas de anos (numéricas) e colunas não numéricas
        colunas_anos = df.columns[df.columns.str.contains(r'\d')]
        colunas_nao_anos = df.columns[~df.columns.str.contains(r'\d')]

        # Combinar colunas duplicadas de anos
        df_combined = df.groupby(level=0, axis=1).sum()
        
        if anos:
            anos_list = anos.split(',')
            anos_list = [ano.strip() for ano in anos_list]  # Remover espaços em branco
        else:
            # Pegar os últimos 10 anos presentes na lista colunas_anos
            anos_list = sorted(colunas_anos)[-5:]
        
        # Verificar se todos os anos fornecidos estão presentes nas colunas de anos identificadas
        if not all(ano in df_combined.columns for ano in anos_list):
            anos_disponiveis = ", ".join(colunas_anos)
            message = f"Os anos fornecidos não estão na tabela. Anos disponíveis: {anos_disponiveis}"
            logging.error(message)
            return HTMLResponse(content=f"{message}", status_code=400)

        # Construir a lista de colunas a serem exibidas
        anos_colunas = list(colunas_nao_anos) + anos_list
        df_combined = df_combined[anos_colunas]

        # Converter o DataFrame em uma tabela HTML
        table_html = tabulate(df_combined, headers='keys', tablefmt='fancy_grid')

        # Retornar a tabela HTML
        return HTMLResponse(content=table_html)
    
    except Exception as e:
        error_message = f"Ocorreu um erro inesperado: {str(e)}"
        logging.error(error_message)
        return HTMLResponse(content=f"{error_message}", status_code=500)

#post para informar o email e a senha cadastrados
@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    """
    Faz login de um usuário e retorna um token JWT se as credenciais forem válidas.

    Recebe as credenciais do usuário e verifica se são válidas. Se forem, retorna um token JWT. 
    Caso contrário, retorna uma mensagem de erro.

    Args:
        user (UserLoginSchema): Credenciais do usuário para login.

    Returns:
        dict: Um dicionário contendo um token JWT ou uma mensagem de erro.
    """
    if check_user(user):
        return sign_jwt(user.email)
    return {
        "error": "Wrong login details!"
    }