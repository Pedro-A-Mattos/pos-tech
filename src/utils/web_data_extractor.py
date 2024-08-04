from fastapi import HTTPException
import logging
from bs4 import BeautifulSoup

def extract_data_from_page(page_content: str):
    """
    Esta função recebe o conteúdo de uma página HTML como uma string, analisa a página
    para encontrar todos os links, filtra os links que começam com "download" e retorna 
    esses links filtrados.

    Args:
        page_content (str): O conteúdo da página HTML a ser analisado.

    Returns:
        list: Uma lista de strings contendo os links filtrados que começam com "download".

    Exceptions:
        Gera um log de erro se ocorrer uma exceção durante o processamento.
    """
    try:
        soup = BeautifulSoup(page_content, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            href = link['href']
            if href.startswith("download"):
                filtered_link = href.split('/')[-1]
        
        logging.info(f"Link filtrado: {filtered_link}")
        return filtered_link

    except Exception as e:
        logging.error(f"Erro durante a extração de links: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def mapear_topicos(page_content: str):
    """
    Esta função recebe o conteúdo da página HTML como uma string, analisa a página 
    para encontrar botões com uma classe específica, filtra os botões com base em uma 
    lista de tópicos relevantes e mapeia os nomes dos tópicos aos seus links.

    Args:
        page_content (str): O conteúdo da página HTML a ser analisado.

    Returns:
        dict: Um dicionário onde as chaves são os nomes dos tópicos relevantes e os 
              valores são os links correspondentes.
    """
    base_link = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao="
    soup = BeautifulSoup(page_content, "html.parser")
    botoes = soup.find_all('button', class_='btn_opt')
    mapeamento = {}
    topicos_relevantes = ['Produção', 'Processamento', 'Comercialização', 'Importação', 'Exportação']
    for botao in botoes:
        nome_topico = botao.text.strip()
        if nome_topico in topicos_relevantes:
            valor_botao = base_link+botao['value']
            mapeamento[nome_topico] = valor_botao
    return mapeamento


def mapear_subopcoes(page_content: str):
    """
    Mapeia as subopções da página HTML para seus respectivos links.

    Esta função recebe o conteúdo de uma página HTML como uma string, analisa a página
    para encontrar botões com uma classe específica, e mapeia os nomes das subopções
    aos seus links completos, incluindo um valor de opção capturado de um campo hidden.

    Args:
        page_content (str): O conteúdo da página HTML a ser analisado.

    Returns:
        dict: Um dicionário onde as chaves são os nomes das subopções e os valores são
              os links correspondentes.
    """
    opcao = capturar_valor_hidden(page_content)
    soup = BeautifulSoup(page_content, "html.parser")
    botoes = soup.find_all('button', class_='btn_sopt')
    mapeamento = {}
    for botao in botoes:
        nome_subopcao = botao.text.strip()
        valor_subopcao = botao['value']
        mapeamento[nome_subopcao] = f'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao={valor_subopcao}&opcao={opcao}'
    return mapeamento



def capturar_valor_hidden(page_content: str):
    """
    Esta função recebe o conteúdo de uma página HTML como uma string, analisa a página 
    para encontrar um campo input do tipo hidden com o nome 'opcao' e retorna seu valor.

    Args:
        page_content (str): O conteúdo da página HTML a ser analisado.

    Returns:
        str: O valor do campo hidden com o nome 'opcao'. Retorna None se o campo não for encontrado.
    """
    soup = BeautifulSoup(page_content, "html.parser")
    input_hidden = soup.find('input', attrs={'type': 'hidden', 'name': 'opcao'})
    if input_hidden:
        return input_hidden['value']
    return None