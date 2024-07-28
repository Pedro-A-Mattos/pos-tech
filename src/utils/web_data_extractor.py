from fastapi import HTTPException
import logging
from bs4 import BeautifulSoup

def extract_data_from_page(page_content: str):
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
            mapeamento[nome_topico] = valor_botao
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