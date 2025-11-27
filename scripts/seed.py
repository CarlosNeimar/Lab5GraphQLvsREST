import json
import random
from faker import Faker

QTD_REGISTROS = 10000  
QTD_USUARIOS = 50      
ARQUIVO_SAIDA = "database.json"

fake = Faker()

def gerar_dados():
    dados = []

    user_ids = [str(i) for i in range(1, QTD_USUARIOS + 1)]

    print(f"Gerando {QTD_REGISTROS} registros...")

    for i in range(1, QTD_REGISTROS + 1):
        registro = {
            "id": str(i),

            "userId": random.choice(user_ids), 

            "score": random.randint(1, 10), 
            "text": fake.sentence(nb_words=random.randint(5, 50)) 
        }
        dados.append(registro)

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=None)
    
    print(f"Sucesso! Arquivo '{ARQUIVO_SAIDA}' gerado com {len(dados)} registros.")

if __name__ == "__main__":
    gerar_dados()