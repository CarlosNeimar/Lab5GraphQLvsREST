import json
import random
from faker import Faker

# Configuração
NUM_USERS = 10000
MAX_POSTS_PER_USER = 10
OUTPUT_FILE = 'database.json'

fake = Faker()

def generate():
    print(f"Gerando {NUM_USERS} usuários e seus posts...")
    data = {"users": [], "posts": []}
    
    # Gerar Usuários
    for i in range(1, NUM_USERS + 1):
        user = {
            "id": i,
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace('\n', ', '),
            "company": fake.company()
        }
        data["users"].append(user)
        
        # Gerar Posts para este usuário
        for j in range(random.randint(0, MAX_POSTS_PER_USER)):
            post = {
                "id": len(data["posts"]) + 1,
                "user_id": i,
                "title": fake.sentence(),
                "content": fake.text(),
                "published": fake.boolean()
            }
            data["posts"].append(post)
            
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f)
    print(f"Dados salvos em {OUTPUT_FILE}")
    print(f"Total Users: {len(data['users'])}")
    print(f"Total Posts: {len(data['posts'])}")

if __name__ == "__main__":
    generate()