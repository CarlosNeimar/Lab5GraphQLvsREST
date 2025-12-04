import requests
import time
import pandas as pd
import random

# Configurações do Experimento
ITERATIONS = 1000  # Quantidade de requisições por cenário
OUTPUT_CSV = 'experiment_results.csv'

# Endpoints
URLS = {
    "Node_REST": "http://localhost:4000",
    "Node_GQL": "http://localhost:4001",
    "Python_REST": "http://localhost:5000",
    "Python_GQL": "http://localhost:5001/graphql"
}

results = []

def run_request(lang, protocol, query_type, url, payload=None, method='GET'):
    start_time = time.perf_counter()
    
    try:
        if method == 'GET':
            response = requests.get(url)
        else:
            response = requests.post(url, json=payload)
        
        end_time = time.perf_counter()
        
        duration_ms = (end_time - start_time) * 1000
        size_bytes = len(response.content)
        
        results.append({
            "language": lang,
            "protocol": protocol,
            "scenario": query_type,
            "response_time_ms": duration_ms,
            "response_size_bytes": size_bytes,
            "status": response.status_code
        })
    except Exception as e:
        print(f"Erro em {lang} {protocol}: {e}")

print("Iniciando Benchmark...")

for i in range(ITERATIONS):
    if i % 10 == 0: print(f"Iteração {i}/{ITERATIONS}")
    
    user_id = random.randint(1, 1000)

    # --- CENÁRIO 1: Fetch Simples (Pegar 1 usuário) ---
    # REST: Pega o objeto inteiro (Overfetching implícito)
    # GQL: Pede apenas nome e email (Fetching exato)
    
    # 1.1 Node REST
    run_request("JS", "REST", "Simple_Fetch", f"{URLS['Node_REST']}/users/{user_id}/full")
    
    # 1.2 Node GraphQL
    gql_query_simple = {
        "query": f'{{ user(id: "{user_id}") {{ name email }} }}'
    }
    run_request("JS", "GraphQL", "Simple_Fetch", URLS['Node_GQL'], payload=gql_query_simple, method='POST')

    # 1.3 Python REST
    run_request("Python", "REST", "Simple_Fetch", f"{URLS['Python_REST']}/users/{user_id}/full")

    # 1.4 Python GraphQL
    run_request("Python", "GraphQL", "Simple_Fetch", URLS['Python_GQL'], payload=gql_query_simple, method='POST')


    # --- CENÁRIO 2: Fetch Complexo (Usuário + Posts) ---
    # REST: Endpoint customizado ou payload completo
    # GQL: Nested query
    
    # 2.1 Node REST (O endpoint /full retorna tudo)
    run_request("JS", "REST", "Complex_Fetch", f"{URLS['Node_REST']}/users/{user_id}/full")
    
    # 2.2 Node GraphQL
    gql_query_complex = {
        "query": f'{{ user(id: "{user_id}") {{ name email posts {{ title content }} }} }}'
    }
    run_request("JS", "GraphQL", "Complex_Fetch", URLS['Node_GQL'], payload=gql_query_complex, method='POST')

    # 2.3 Python REST
    run_request("Python", "REST", "Complex_Fetch", f"{URLS['Python_REST']}/users/{user_id}/full")

    # 2.4 Python GraphQL
    run_request("Python", "GraphQL", "Complex_Fetch", URLS['Python_GQL'], payload=gql_query_complex, method='POST')

# Salvar
df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Benchmark finalizado. Resultados salvos em {OUTPUT_CSV}")