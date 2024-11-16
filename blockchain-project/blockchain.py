import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #Criar o bloco gênesis
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Cria um novo bloco na Blockchain
        :param proof: <int> A prova fornecida pelo PoW
        :param previous_hash: (Opcional) <str> Hash do bloco anterior
        :return: <dict> Novo bloco
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []

        self.chain.append(block)
        
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        Cria uma nova transação para ir para o próximo bloco minerado
        :param sender: <str> Endereço do remetente
        :param recipient: <str> Endereço do destinatário
        :param amount: <int> Quantidade
        :return: <int> O índice do bloco que armazenará esta transação
        """
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            }
        )

        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        """
        Cria um hash SHA-256 de um bloco
        :param block: <dict> Bloco
        :return: <str>
        """
        
        #Ordenando o dicionário (evitar hashes inconsistentes)
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def proof_of_work(self, last_block):
        """
        Algoritmo de prova de trabalho:
        - Encontre um número p' tal que hash(pp') contenha 4 zeros à esquerda
        - p é a prova do bloco anterior , e p' é a nova prova
        :param last_proof: <int>
        :return: <int>
        """
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0

        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Valida a prova: verifica se hash(last_proof, proof) contém 4 zeros à esquerda
        :param last_proof: <int> Prova anterior
        :param proof: <int> Prova atual
        :return: <bool> TRUE se correto, FALSE se não
        """
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        prev_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{prev_block}')
            print(f'{block}')
            print("\n-----------\n")

            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(prev_block):
                return False
            
            # Check that the Proof of Work is correct
            if not self.valid_proof(prev_block['proof'], block['proof']):
                return False
            
            prev_block = block
            current_index += 1

        return True

    def mine(self, current_transactions):
        # Executamos o pow para obter a próxima prova...
        last_block  = self.last_block
        proof = self.proof_of_work(last_block)

        for transaction in current_transactions:
            self.new_transaction(
                sender=transaction['sender'],
                recipient=transaction['recipient'],
                amount=transaction['value']
            )

        # Devemos receber uma recompensa por encontrar a prova.
        # Por enquanto, não estamos em rede, então o único beneficiário é ELE
        # O remetente é "0" para significar que este nó minerou uma nova moeda.
        self.new_transaction(
            sender="0",
            recipient="nakamoto",
            amount=1
        )

        # Minera o novo bloco adicionando-o à cadeia
        previous_hash = self.hash(last_block)
        block = self.new_block(proof, previous_hash)

    def print_chain(self):
        current_index = 1

        print("Blockchain={")

        while current_index < len(self.chain):
            block = self.chain[current_index]
            print(json.dumps(block, indent=4))
            current_index += 1

        print("}")

    def return_blockchain_json(self):
        blockchain = {"Blocos": {}}
        current_index = 1
        
        while current_index < len(self.chain):
            block = self.chain[current_index]
            blockchain["Blocos"][block["index"]] = json.dumps(block)
            current_index += 1

        blockchain_json = json.dumps(blockchain)

        return blockchain_json
    
#blockchain = Blockchain()
#
#current_transactions = [{
#    "sender": "Joao",
#    "recipient": "Pedro",
#    "value": 5
#}]
#
#for i in range(0, 20):
#    blockchain.mine(current_transactions)
#
#blockchain.print_chain()