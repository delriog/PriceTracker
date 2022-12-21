from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json

def buscaProduto(url: str): # Endpoint to get the data from a product

    driver = webdriver.Edge()

    driver.get(url["link"]) # opens the url

    div_mae = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ppd"]')))

    html_content = div_mae.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')

    titulo_produto = soup.select("span[id^=productTitle]") # Get the title
    titulo_produto = titulo_produto[0].get_text()
    titulo_produto = titulo_produto.strip()


    preco_produto = soup.find_all("span", class_="a-offscreen") # Get the price
    preco_produto = preco_produto[0].get_text()
    preco_produto = preco_produto.replace("R$", "")
    preco_produto = preco_produto.replace(".","")
    preco_produto = preco_produto.replace(",",".")



    driver.quit() # Close the window

    responseHeaders = { # Header with all the data
        "titulo": titulo_produto,
        "preco": preco_produto
    }
    return responseHeaders # Response

# buscaProduto("https://www.amazon.com.br/Novo-Echo-Dot-4%C2%AA-gera%C3%A7%C3%A3o/dp/B084DWCZY6/ref=asc_df_B084DWCZY6/?tag=googleshopp00-20&linkCode=df0&hvadid=404840237192&hvpos=&hvnetw=g&hvrand=3274971502365317293&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9102201&hvtargid=pla-989629063328&psc=1")

def atualizaProduto(dados): # Endpoint to update the products

    lista_dados = list(dados) 

    produtos_atualizados = []
    for index, produto in enumerate(lista_dados): # For each product
        produto = list(produto)

        driver = webdriver.Edge()

        driver.get(produto[2]) # Open the product link

        div_mae = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ppd"]')))

        html_content = div_mae.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content, 'html.parser')

        titulo_produto = soup.select("span[id^=productTitle]") # Get the title
        titulo_produto = titulo_produto[0].get_text() 
        titulo_produto = titulo_produto.strip()


        preco_produto = soup.find_all("span", class_="a-offscreen") # Get the price
        preco_produto = preco_produto[0].get_text()
        preco_produto = preco_produto.replace("R$", "")
        preco_produto = preco_produto.replace(".","")
        preco_produto = preco_produto.replace(",",".")

        
        if float(preco_produto) < float(produto[1]): # If the product have discount append the product to a list and save the new price
            print("produt[1]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", lista_dados[index])
            lista_dados[index] = (produto[0], preco_produto, produto[2])
            produtos_atualizados.append(produto[2])


        driver.quit() # Close the window
    
    responseHeaders = { # Header with all the data
                "produtos": lista_dados,
                "descontos": produtos_atualizados
            }

    return responseHeaders # Response


    