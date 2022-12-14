import pandas as pd
from flask import Flask, request, jsonify, abort
import coletor
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

if __name__ == '__main__':
   app.run("127.0.0.1","8080", True)
