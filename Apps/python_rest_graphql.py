import json
from flask import Flask, jsonify, request
from ariadne import gql, QueryType, make_executable_schema, graphql_sync
from ariadne.explorer import ExplorerGraphiQL

# Carregamento da base de dados
try:
    with open('database.json', 'r', encoding='utf-8') as f:
        COMMENTS_DATA = json.load(f)
    print(f"[PY] Base de dados carregada com {len(COMMENTS_DATA)} registros.")
except FileNotFoundError:
    print("[PY] ERRO: Arquivo 'database.json' não encontrado. Rode o seed.py primeiro.")
    COMMENTS_DATA = []

app = Flask(__name__)

# --- ENDPOINTS REST ---

@app.route('/rest/comments', methods=['GET'])
def rest_all_comments():
    return jsonify(COMMENTS_DATA)

@app.route('/rest/comments/<string:id>', methods=['GET'])
def rest_comment_by_id(id):
    # next() retorna o primeiro item encontrado ou None
    comment = next((c for c in COMMENTS_DATA if c['id'] == id), None)
    return jsonify(comment)

@app.route('/rest/comments/user/<string:user_id>', methods=['GET'])
def rest_comments_by_user_id(user_id):
    comments = [c for c in COMMENTS_DATA if c['userId'] == user_id]
    return jsonify(comments)

@app.route('/rest/comments/min-score/<int:score>', methods=['GET'])
def rest_comments_by_min_score(score):
    comments = [c for c in COMMENTS_DATA if c['score'] >= score]
    return jsonify(comments)

# --- CONFIGURAÇÃO GRAPHQL ---

type_defs = gql("""
    type Comment {
        id: ID!
        userId: ID!
        score: Int
        text: String
    }

    type Query {
        allComments: [Comment]
        commentById(id: ID!): Comment
        commentsByUserId(id: ID!): [Comment]
        commentsByMinScore(score: Int!): [Comment]
    }
""")

query = QueryType()

@query.field("allComments")
def resolve_all_comments(*_):
    return COMMENTS_DATA

@query.field("commentById")
def resolve_comment_by_id(*_, id):
    return next((c for c in COMMENTS_DATA if c['id'] == id), None)

@query.field("commentsByUserId")
def resolve_comments_by_user_id(*_, id):
    return [c for c in COMMENTS_DATA if c['userId'] == id]

@query.field("commentsByMinScore")
def resolve_comments_by_min_score(*_, score):
    return [c for c in COMMENTS_DATA if c['score'] >= score]

schema = make_executable_schema(type_defs, query)

# Interface Gráfica do GraphQL (Playground)
explorer_html = ExplorerGraphiQL().html(None)

# Rota única para GraphQL (GET para playground, POST para consultas)
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=True
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

# --- INICIALIZAÇÃO DO SERVIDOR ---

if __name__ == "__main__":
    # Usando o runner nativo do Flask para evitar conflitos WSGI/ASGI
    # debug=False para o benchmark ser mais justo (menos overhead de debug)
    print("[PY] Servidor rodando em http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=False)