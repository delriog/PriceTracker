import pandas as pd
from flask import Flask, request, jsonify, abort
import coletor
import csv
import json

app = Flask(__name__)
filename = 'dados.json'

@app.route("/cadastraproduto", methods = ["GET"])
def getDadosProduto():
    dados = coletor.buscaProduto(request.headers)
    produto = request.headers

    linha = [ produto["id"], produto["link"], dados["titulo"], dados["preco"]]

    df = pd.read_csv('dados.csv')
    df.loc[len(df)] = linha

    df.to_csv('dados.csv',index=False)    
    
    return jsonify(dados)



@app.route("/verificaproduto", methods = ["GET"])
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

@app.route("/retornaprodutos", methods = ["GET"])
def getProdutosCadastrados():
    usuario = request.headers

    id = int(usuario["id"])
    print("type id>", type(id))
    print("id>>>>>>>>>>>", id)
    df = pd.read_csv('dados.csv')

    responseHeaders = {
                "resposta": "ok",
            }
    
    linhas = df.loc[df["id"] == id]

    lst_tuple = list(zip(linhas["nome"].values, linhas["preco"].values))
    print(lst_tuple)
    return jsonify(lst_tuple)


if __name__ == '__main__':
   app.run("127.0.0.1","8080", True)
