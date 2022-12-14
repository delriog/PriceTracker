from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json

def buscaProduto(url: str):

    driver = webdriver.Edge()

    driver.get(url["link"])

    div_mae = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ppd"]')))

    html_content = div_mae.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')

    titulo_produto = soup.select("span[id^=productTitle]")
    titulo_produto = titulo_produto[0].get_text()
    titulo_produto = titulo_produto.strip()


    preco_produto = soup.find_all("span", class_="a-offscreen")
    preco_produto = preco_produto[0].get_text()
    preco_produto = preco_produto.replace("R$", "")
    preco_produto = preco_produto.replace(",",".")

    print(titulo_produto, preco_produto)

    driver.quit()

    responseHeaders = {
        "titulo": titulo_produto,
        "preco": preco_produto
    }
    return responseHeaders

# buscaProduto("https://www.amazon.com.br/Novo-Echo-Dot-4%C2%AA-gera%C3%A7%C3%A3o/dp/B084DWCZY6/ref=asc_df_B084DWCZY6/?tag=googleshopp00-20&linkCode=df0&hvadid=404840237192&hvpos=&hvnetw=g&hvrand=3274971502365317293&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9102201&hvtargid=pla-989629063328&psc=1")