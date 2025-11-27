import requests
import time
import csv
import argparse
import json
import os


analisador = argparse.ArgumentParser(description='Benchmark de performance REST vs GraphQL')
analisador.add_argument('--modo', choices=['python', 'javascript'], required=True, help="Modo de linguagem (backend)")
args = analisador.parse_args()


URL_BASE_REST = ""
URL_GRAPHQL = ""

if args.modo == 'python':

    URL_BASE_REST = "http://localhost:8080/rest/comments"
    URL_GRAPHQL = "http://localhost:8080/graphql"
else: 

    URL_BASE_REST = "http://localhost:3000/comments"
    URL_GRAPHQL = "http://localhost:3001/"


ENDPOINTS_REST = [
    {"nome": "todosComentarios", "url": URL_BASE_REST},
    {"nome": "comentarioPorId", "url": f"{URL_BASE_REST}/4"},
    {"nome": "comentariosPorUsuarioId", "url": f"{URL_BASE_REST}/user/13"},
    {"nome": "comentariosPorPontuacaoMinima", "url": f"{URL_BASE_REST}/min-score/5"},
]


CONSULTAS_GRAPHQL = [
    {"nome": "todosComentarios", "consulta": "{ allComments { id } }"},
    {"nome": "comentarioPorId", "consulta": "query($id: ID!) { commentById(id: $id) { id } }", "variaveis": {"id": "4"}},
    {"nome": "comentariosPorUsuarioId", "consulta": "query($id: ID!) { commentsByUserId(id: $id) { id } }",
     "variaveis": {"id": "13"}},
    {"nome": "comentariosPorPontuacaoMinima", "consulta": "query($score: Int!) { commentsByMinScore(score: $score) { id } }",
     "variaveis": {"score": 5}},
]


respostas_graphql = []
respostas_rest = []


def contar_caracteres_json(array_json):
    string_json_combinada = json.dumps(array_json)

    return sum(1 for caractere in string_json_combinada if not caractere.isspace())

def avaliar_desempenho_rest():
    resultados = []
    print("  - Avaliando REST...")
    for endpoint in ENDPOINTS_REST:
        print(f"    -> Testando endpoint: {endpoint['nome']}")
        for _ in range(100):
            try:
                inicio = time.time()
                resposta = requests.get(endpoint["url"])
                fim = time.time()
                
                if resposta.status_code == 200:
                    respostas_rest.append(resposta.json())
                    resultados.append({
                        "consulta": endpoint["nome"],
                        "status_code": resposta.status_code,
                        "tempo_resposta_ms": (fim - inicio) * 1000,
                    })
                else:
                    print(f"    [Aviso] REST endpoint {endpoint['nome']} falhou com status {resposta.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"  [ERRO] Não foi possível conectar ao servidor REST em {endpoint['url']}. O servidor está rodando?")
                return [] 
    return resultados


def avaliar_desempenho_graphql():
    resultados = []
    print("  - Avaliando GraphQL...")
    for item in CONSULTAS_GRAPHQL:
        print(f"    -> Testando query: {item['nome']}")
        for _ in range(100):
            try:
                inicio = time.time()
 
                resposta = requests.post(URL_GRAPHQL, json={
                    "query": item["consulta"],
                    "variables": item.get("variaveis", {}),
                })
                fim = time.time()

                if resposta.status_code == 200:
                    r_json = resposta.json()
                    # Verifica se o GraphQL retornou erros no corpo
                    if 'errors' in r_json:
                         print(f"    [Erro GraphQL] {r_json['errors'][0]['message']}")
                    
                    respostas_graphql.append(r_json)
                    resultados.append({
                        "consulta": item["nome"],
                        "status_code": resposta.status_code,
                        "tempo_resposta_ms": (fim - inicio) * 1000,
                    })
                else:
                      print(f"    [Aviso] GraphQL query {item['nome']} falhou com status {resposta.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"  [ERRO] Não foi possível conectar ao servidor GraphQL em {URL_GRAPHQL}. O servidor está rodando?")
                return [] 
    return resultados


def salvar_em_csv(nome_arquivo, dados, nomes_campos):
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=nomes_campos)
        escritor.writeheader()
        escritor.writerows(dados)


# Bloco principal de execução
if __name__ == "__main__":
    
    # Prepara diretórios
    print(f"Preparando diretórios de resultados para o modo: {args.modo}...")
    caminho_tempo = f"results/{args.modo}/response_time"
    caminho_tamanho = f"results/{args.modo}/response_size"
    
    os.makedirs(caminho_tempo, exist_ok=True)
    os.makedirs(caminho_tamanho, exist_ok=True)

    campos_tempo = ["consulta", "status_code", "tempo_resposta_ms"]
    campos_tamanho = ["protocolo", "tamanho_total_resposta"]

    # --- Benchmark REST ---
    print(f"Avaliando desempenho REST no modo {args.modo}...")
    resultados_rest = avaliar_desempenho_rest()
    
    if resultados_rest:
        salvar_em_csv(f"{caminho_tempo}/rest_results.csv", resultados_rest, campos_tempo)
        
        salvar_em_csv(f"{caminho_tamanho}/rest_results.csv",
        [{"protocolo": "rest", "tamanho_total_resposta": contar_caracteres_json(respostas_rest)}],
            campos_tamanho
        )
        print("  - Resultados REST salvos.")
    else:
        print("  - Avaliação REST pulada ou falhou.")


    # --- Benchmark GraphQL ---
    print(f"Avaliando desempenho GraphQL no modo {args.modo}...")
    resultados_graphql = avaliar_desempenho_graphql()
    
    if resultados_graphql:
        salvar_em_csv(f"{caminho_tempo}/graphql_results.csv", resultados_graphql, campos_tempo)

        salvar_em_csv(f"{caminho_tamanho}/graphql_results.csv",
        [{"protocolo": "graphql", "tamanho_total_resposta": contar_caracteres_json(respostas_graphql)}],
            campos_tamanho
        )
        print("  - Resultados GraphQL salvos.")
    else:
        print("  - Avaliação GraphQL pulada ou falhou.")

    print("\nBenchmark concluído.")