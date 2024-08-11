import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fastapi import HTTPException
from src.utils.browser_automation import get_webdriver

def test_chromedriver_initialization():
    """
    Testa se o ChromeDriver pode ser inicializado corretamente.
    """
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.quit()
    except Exception as e:
        pytest.fail(f"Falha ao iniciar o ChromeDriver: {e}")
        
        
def test_get_webdriver_valid_url():
    """
    Testa a função get_webdriver com uma URL válida.
    Testa se é possível coletar o código HTML de uma página web.
    """
    url = "http://vitibrasil.cnpuv.embrapa.br"
    try:
        content = get_webdriver(url)
        assert "<html" in content.lower() 
    except HTTPException as e:
        pytest.fail(f"Falha ao coletar o código HTML da página: {e}")