from blockchain import *

blockchain = Blockchain()

current_transactions = [{
    "sender": "Joao",
    "recipient": "Pedro",
    "value": 5
}]

for i in range(0, 1):
    blockchain.mine(current_transactions)

blockchain.print_chain()
