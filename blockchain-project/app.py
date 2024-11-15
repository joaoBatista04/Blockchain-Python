from flask import Flask, request, jsonify, redirect, url_for

from flask_cors import CORS
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()
added_transactions = []

# Função para somar dois números
def somar(a, b):
    return a + b

@app.route('/addtransfer', methods=['POST'])
def add_transfer():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados JSON não recebidos."}), 400
    
    sender = dados.get('sender')
    recipient = dados.get('recipient')
    value = dados.get('value')

    new_transaction = {
        'sender': sender,
        'recipient': recipient,
        'value': value
    }

    added_transactions.append(new_transaction)

    return jsonify({
        "id": len(added_transactions),
        "sender": sender,
        "recipient": recipient,
        "value": value
    })

@app.route('/miner', methods=["GET"])
def miner_block():
    global added_transactions

    blockchain.mine(added_transactions)

    added_transactions = []

    blockchain_json = blockchain.return_blockchain_json()

    return jsonify(blockchain_json)

# Inicializa a aplicação
if __name__ == '__main__':
    app.run(debug=True)