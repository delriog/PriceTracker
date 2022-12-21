import pandas as pd
from flask import Flask, request, jsonify, abort
import coletor
import csv
import json

app = Flask(__name__)
filename = 'dados.json'

@app.route("/cadastraproduto", methods = ["GET"]) # Endpoint that register new products
def getDadosProduto():
    dados = coletor.buscaProduto(request.headers)
    produto = request.headers

    linha = [ produto["id"], produto["link"], dados["titulo"], dados["preco"]]

    df = pd.read_csv('dados.csv')
    df.loc[len(df)] = linha

    df.to_csv('dados.csv',index=False)    
    
    return jsonify(dados)



@app.route("/verificaproduto", methods = ["GET"]) # Endpoint that verify is the product is alredy registered
def getEstadoProduto():
    produto = request.headers

    link = produto["link"]

    df = pd.read_csv('dados.csv')

    responseHeaders = {
                "resposta": "ok",
            }

    for link_dataset in df['link'].tolist():
        if link == link_dataset: 
            responseHeaders = {
                "resposta": "not",
            }

    return jsonify(responseHeaders)

@app.route("/retornaprodutos", methods = ["GET"]) # Endpoint that update the products and return if have discount
def getProdutosCadastrados():
    usuario = request.headers

    id = int(usuario["id"])
    df = pd.read_csv('dados.csv') # get the data

    responseHeaders = {
                "resposta": "ok",
            }
    
    linhas = df.loc[df["id"] == id] # filter only the lines that have the same id as the user

    dados = list(zip(linhas["nome"].values, linhas["preco"].values, linhas["link"].values))
    print("Dados do server: ", dados)
    dados_atualizados = coletor.atualizaProduto(dados) # Sends to the collector the products




    for id_dataset in df['id'].tolist(): # Update de database
        print("id_dataset", id_dataset) 
        for i in dados_atualizados["produtos"]:
            if id == id_dataset: 
                df.loc[(df['link'] == i[2]) & (df["id"] == id), "preco"] = i[1]


    df.to_csv('dados.csv',index=False)     

    
    return jsonify(dados_atualizados) #return the updated data


if __name__ == '__main__':
   app.run("127.0.0.1","8080", True)
