from fastapi import HTTPException
import logging
from bs4 import BeautifulSoup

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
        raise HTTPException(status_code=500, detail=str(e))
