
from flask import Flask, request, jsonify, abort
import coletor

app = Flask(__name__)

@app.route("/produto", methods = ["GET"])
def getDadosProduto():
    dados = coletor.buscaProduto(request.headers)
    return jsonify(dados)

if __name__ == '__main__':
   app.run("127.0.0.1","8080", True)