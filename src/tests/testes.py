from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
from bs4 import BeautifulSoup
import requests
import os

logging.basicConfig(level=logging.INFO)

def extract_data_from_page(page_content: str):
    try:
        soup = BeautifulSoup(page_content, "html.parser")
        links = soup.find_all("a", href=True)

        filtered_links = []
        for link in links:
            href = link['href']
            logging.info(f"Link encontrado: {href}")
            if href.startswith("download"):
                filtered_links.append(href)
        
        logging.info(f"Links filtrados: {filtered_links}")
        return filtered_links

    except Exception as e:
        logging.error(f"Erro durante a extração de links: {e}")


def get_webdriver(url: str):
    """
    Função que faz web scraping em uma página web especificada pela URL.

    Args:
        url (str): A URL da página web a ser raspada.

    Returns:
        str: O conteúdo da página web em formato HTML.

    Raises:
        HTTPException: Se ocorrer qualquer erro durante o processo de scraping.
    """
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Inicia o webdriver do Chrome
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        page_content = driver.page_source
        driver.quit()

        return page_content

    except Exception as e:
        logging.error(f"Erro durante o scraping: {e}")

def download_file(link: str, base_url: str, save_path: str):
    try:
        # Se o link for relativo, adicione o base_url
        if not link.startswith("http"):
            link = os.path.join(base_url, link)

        response = requests.get(link)
        response.raise_for_status()  # Verifica se houve algum erro na requisição

        with open(save_path, 'wb') as file:
            file.write(response.content)

        logging.info(f"Arquivo baixado com sucesso: {save_path}")

    except Exception as e:
        logging.error(f"Erro durante o download do arquivo: {e}")

# Função para mapear os tópicos aos valores dos botões
def mapear_topicos(page_content: str):
    base_link = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao="
    soup = BeautifulSoup(page_content, "html.parser")
    botoes = soup.find_all('button', class_='btn_opt')
    mapeamento = {}
    topicos_relevantes = ['Produção', 'Processamento', 'Comercialização', 'Importação', 'Exportação']
    for botao in botoes:
        nome_topico = botao.text.strip()
        if nome_topico in topicos_relevantes:
            valor_botao = base_link+botao['value']
            mapeamento[nome_topico] = valor_botao= valor_botao
    return mapeamento

# Função para mapear as subopções
def mapear_subopcoes(page_content: str):
    opcao = capturar_valor_hidden(page_content)
    soup = BeautifulSoup(page_content, "html.parser")
    botoes = soup.find_all('button', class_='btn_sopt')
    mapeamento = {}
    for botao in botoes:
        nome_subopcao = botao.text.strip()
        valor_subopcao = botao['value']
        mapeamento[nome_subopcao] = f'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao={valor_subopcao}&opcao={opcao}'
    return mapeamento


# Função para capturar o valor do input hidden
def capturar_valor_hidden(page_content: str):
    soup = BeautifulSoup(page_content, "html.parser")
    input_hidden = soup.find('input', attrs={'type': 'hidden', 'name': 'opcao'})
    if input_hidden:
        return input_hidden['value']
    return None

if __name__ == "__main__":
    # url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"  
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"
    base_url = "http://vitibrasil.cnpuv.embrapa.br/" 

    page_content = get_webdriver(url)
    teste = mapear_topicos(page_content)
    # teste = mapear_subopcoes(page_content)

    print(teste)
    # filtered_links = extract_data_from_page(page_content)


    # if filtered_links:
    #     download_link = filtered_links[0]
    #     save_path = "../storage/Producao.csv"  
    #     download_file(download_link, base_url, save_path)
    # else:
    #     logging.info("Nenhum link para download encontrado.")
