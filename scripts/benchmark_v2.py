import requests
import time
import pandas as pd
import random

ITERATIONS = 100
OUTPUT_CSV = 'results_v2.csv'

URLS = {
    "Node_REST": "http://localhost:4000",
    "Node_GQL": "http://localhost:4001",
    "Python_REST": "http://localhost:5000",
    "Python_GQL": "http://localhost:5001/graphql"
}

results = []

def measure_request(url, payload=None, method='GET'):
    """Executa uma req e retorna (tempo_ms, tamanho_bytes, status)"""
    start_time = time.perf_counter()
    try:
        if method == 'GET':
            response = requests.get(url)
        else:
            response = requests.post(url, json=payload)
        
        duration_ms = (time.perf_counter() - start_time) * 1000
        return duration_ms, len(response.content), response.status_code
    except Exception as e:
        print(f"Erro: {e}")
        return 0, 0, 500

print("Iniciando Benchmark V2 (Com cenário Real World)...")

for i in range(ITERATIONS):
    if i % 20 == 0: print(f"Iteração {i}/{ITERATIONS}")
    
    user_id = random.randint(1, 1000)

    # ==============================================================================
    # CENÁRIO 1: OVER-FETCHING (REST traz tudo vs GraphQL traz só o necessário)
    # ==============================================================================
    
    # Node REST (Traz tudo)
    t, s, st = measure_request(f"{URLS['Node_REST']}/users/{user_id}/full")
    results.append({"lang": "JS", "proto": "REST", "scenario": "Overfetch_Scenario", "ms": t, "bytes": s})
    
    # Node GraphQL (Traz só nome e email)
    gql_q = {"query": f'{{ user(id: "{user_id}") {{ name email }} }}'}
    t, s, st = measure_request(URLS['Node_GQL'], payload=gql_q, method='POST')
    results.append({"lang": "JS", "proto": "GraphQL", "scenario": "Overfetch_Scenario", "ms": t, "bytes": s})

    # Python REST & GraphQL (Mesma lógica acima)
    t, s, st = measure_request(f"{URLS['Python_REST']}/users/{user_id}/full")
    results.append({"lang": "Python", "proto": "REST", "scenario": "Overfetch_Scenario", "ms": t, "bytes": s})
    
    t, s, st = measure_request(URLS['Python_GQL'], payload=gql_q, method='POST')
    results.append({"lang": "Python", "proto": "GraphQL", "scenario": "Overfetch_Scenario", "ms": t, "bytes": s})


    # ==============================================================================
    # CENÁRIO 2: REAL WORLD / UNDER-FETCHING (N+1 Requests)
    # Aqui comparamos: 1 Query GraphQL Complexa VS 2 Calls REST
    # ==============================================================================

    # --- Lado do GraphQL (1 Chamada traz User + Posts) ---
    gql_complex = {"query": f'{{ user(id: "{user_id}") {{ name email posts {{ title }} }} }}'}
    
    # JS GraphQL
    t, s, st = measure_request(URLS['Node_GQL'], payload=gql_complex, method='POST')
    results.append({"lang": "JS", "proto": "GraphQL", "scenario": "RealWorld_Complex", "ms": t, "bytes": s})
    
    # Python GraphQL
    t, s, st = measure_request(URLS['Python_GQL'], payload=gql_complex, method='POST')
    results.append({"lang": "Python", "proto": "GraphQL", "scenario": "RealWorld_Complex", "ms": t, "bytes": s})


    # --- Lado do REST (2 Chamadas: 1 pra User, 1 pra Posts) ---
    
    # JS REST (Encadeado)
    
    # Chamada 1: Pega metadados do user
    t1, s1, st1 = measure_request(f"{URLS['Node_REST']}/users/{user_id}/full") 
    # Chamada 2: Pega posts especificamente
    t2, s2, st2 = measure_request(f"{URLS['Node_REST']}/users/{user_id}/posts")
    
    results.append({
        "lang": "JS", 
        "proto": "REST", 
        "scenario": "RealWorld_Complex", 
        "ms": t1 + t2,        # SOMA DOS TEMPOS
        "bytes": s1 + s2      # SOMA DOS TAMANHOS (Trafego total de rede)
    })

    # Python REST (Encadeado)
    t1, s1, st1 = measure_request(f"{URLS['Python_REST']}/users/{user_id}/full")
    t2, s2, st2 = measure_request(f"{URLS['Python_REST']}/users/{user_id}/posts")
    
    results.append({
        "lang": "Python", 
        "proto": "REST", 
        "scenario": "RealWorld_Complex", 
        "ms": t1 + t2, 
        "bytes": s1 + s2
    })

    # ==============================================================================
    # CENÁRIO 3: O TEMIDO "N+1" (Listagem)
    # ==============================================================================
    LIMIT = 10 

    # --- Lado do GraphQL ---
    # AGORA PASSAMOS O LIMIT NA QUERY
    gql_n_plus_one = {
        "query": f'{{ users(limit: {LIMIT}) {{ id name posts {{ title }} }} }}'
    }
    
    t, s, st = measure_request(URLS['Node_GQL'], payload=gql_n_plus_one, method='POST')
    results.append({"lang": "JS", "proto": "GraphQL", "scenario": "N_Plus_One_List", "ms": t, "bytes": s})
    
    t, s, st = measure_request(URLS['Python_GQL'], payload=gql_n_plus_one, method='POST')
    results.append({"lang": "Python", "proto": "GraphQL", "scenario": "N_Plus_One_List", "ms": t, "bytes": s})


    # --- Lado do REST (N+1 Chamadas) ---
    
    # Passo 1: Buscar a lista (REST não implementamos limit, traz tudo, mas é rápido pq é flat)
    start_total = time.perf_counter()
    resp = requests.get(f"{URLS['Node_REST']}/users") 
    users_list = resp.json() 
    total_bytes = len(resp.content) 
    
    # Passo 2: Iterar nos 10
    for i in range(LIMIT):
        u_id = users_list[i]['id']
        r_posts = requests.get(f"{URLS['Node_REST']}/users/{u_id}/posts")
        total_bytes += len(r_posts.content)
        
    end_total = time.perf_counter()
    total_ms = (end_total - start_total) * 1000
    
    results.append({
        "lang": "JS", 
        "proto": "REST", 
        "scenario": "N_Plus_One_List", 
        "ms": total_ms, 
        "bytes": total_bytes
    })

    # Repetir para Python REST...
    start_total = time.perf_counter()
    resp = requests.get(f"{URLS['Python_REST']}/users")
    users_list = resp.json()
    total_bytes = len(resp.content)
    
    for i in range(LIMIT):
        u_id = users_list[i]['id']
        r_posts = requests.get(f"{URLS['Python_REST']}/users/{u_id}/posts")
        total_bytes += len(r_posts.content)
        
    end_total = time.perf_counter()
    total_ms = (end_total - start_total) * 1000
    
    results.append({
        "lang": "Python", 
        "proto": "REST", 
        "scenario": "N_Plus_One_List", 
        "ms": total_ms, 
        "bytes": total_bytes
    })

# Salvar
df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Benchmark V2 finalizado. Resultados em {OUTPUT_CSV}")