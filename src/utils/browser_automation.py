from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

        # Usando webdriver-manager para gerenciar o ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        page_content = driver.page_source
        driver.quit()

        return page_content

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))