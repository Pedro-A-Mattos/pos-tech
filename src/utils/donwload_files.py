from fastapi import HTTPException
import requests
import logging
import os

def download_file(link: str, base_url: str, save_path: str):
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