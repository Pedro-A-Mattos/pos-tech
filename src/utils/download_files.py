from fastapi import HTTPException
import requests
import logging
import os

def download_file(link: str, base_url: str, save_path: str):
    """
    Faz o download de um arquivo a partir de um link e o salva no caminho especificado.

    Esta função recebe um link para download, uma URL base e um caminho onde o arquivo 
    deve ser salvo. Se o link for relativo, ele será combinado com a URL base. Em seguida,
    a função faz o download do arquivo e o salva no local especificado.

    Args:
        link (str): O link para o arquivo a ser baixado.
        base_url (str): A URL base a ser usada se o link for relativo.
        save_path (str): O caminho onde o arquivo deve ser salvo.

    Exceptions:
        Gera um log de erro se ocorrer uma exceção durante o download ou salvamento do arquivo.
    """
    try:
        if not link.startswith("http"):
            link = os.path.join(base_url, link)
            
        response = requests.get(link)
        response.raise_for_status()  

        base_dir = os.path.dirname(os.path.dirname(__file__))
        save_path = os.path.join(base_dir, 'src', save_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as file:
            file.write(response.content)

        logging.info(f"Arquivo baixado com sucesso: {save_path}")

    except Exception as e:
        logging.error(f"Erro durante o download do arquivo: {e}")
        raise HTTPException(status_code=500, detail=str(e))