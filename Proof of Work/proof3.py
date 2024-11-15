import hashlib

# Mensagem base (pode ser qualquer string inicial)
mensagem = "ChatGPT"
zeros = "0000000"  # Número de zeros no início que queremos
nonce = 0  # Contador para achar a entrada

while True:
    # Concatenando a mensagem base com o nonce para gerar uma nova string
    tentativa = f"{mensagem}{nonce}"
    # Calculando o SHA-256 da string tentativa
    hash_result = hashlib.sha256(tentativa.encode()).hexdigest()
    
    # Verificando se o hash começa com 8 zeros
    if hash_result.startswith(zeros):
        print(f"Entrada encontrada: {tentativa}")
        print(f"Hash correspondente: {hash_result}")
        break
    nonce += 1
