from fastapi import FastAPI, HTTPException, Query  # Importa classes e funções necessárias do FastAPI
import logging  # Importa a biblioteca de logging para registrar informações e erros
from utils.browser_automation import get_webdriver  # Importa função de scraping de sites
from utils.web_data_extractor import extract_data_from_page
app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# Configura o logging para registrar informações e erros
logging.basicConfig(level=logging.INFO)

# Define uma rota GET para obter links do website
@app.get("/links/")
async def get_website_links():
    """
    Rota GET para obter links do primeiro nível de um website.

    Returns:
        dict: Um dicionário contendo uma lista de links encontrados.

    Raises:
        HTTPException: Se nenhum conteúdo ou link for encontrado.
    """
    # Faz o scraping do site especificado
    website_content = get_webdriver("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01")

    # Verifica se há conteúdo no site
    if not website_content:
        # Lança uma exceção HTTP 404 se nenhum conteúdo for encontrado
        raise HTTPException(status_code=404, detail="Nenhum conteúdo encontrado")
    

@app.get("/links2/")
async def get_website_links2(link: str = Query(..., description="URL do link para acessar")):
    """
    Rota GET para obter links do segundo nível de um website.

    Args:
        link (str): A URL do link para acessar.

    Returns:
        dict: Um dicionário contendo uma lista de links encontrados.

    Raises:
        HTTPException: Se o parâmetro 'link' estiver ausente, ou se nenhum conteúdo ou link for encontrado.
    """
    # Registra o link recebido
    logging.info(f"Recebendo link: {link}")

    # Verifica se o link foi recebido corretamente
    if not link:
        # Lança uma exceção HTTP 400 se o parâmetro 'link' estiver ausente
        raise HTTPException(status_code=400, detail="Parâmetro 'link' é obrigatório")

    # Faz o scraping do site especificado pelo link
    website_content = get_webdriver(link)
    teste = extract_data_from_page(website_content)
    # Verifica se há conteúdo no site
    if not website_content:
        # Lança uma exceção HTTP 404 se nenhum conteúdo for encontrado
        raise HTTPException(status_code=404, detail="Nenhum conteúdo encontrado")

    # Retorna os links extraídos como resposta
    return {"content": teste}