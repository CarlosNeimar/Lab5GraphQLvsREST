import json
from ariadne import ObjectType, QueryType, gql, make_executable_schema, graphql_sync
from flask import Flask, request, jsonify

# Carregar dados
try:
    with open('../Data/database_100k_user.json', 'r') as f:
        db = json.load(f)
except FileNotFoundError:
    print("ERRO: O arquivo '../Data/database_100k_user.json' não foi encontrado. Execute 'generate_data.py' primeiro.")
    exit(1)

type_defs = gql("""
    type Post {
        id: ID!
        title: String
        content: String
        published: Boolean
    }

    type User {
        id: ID!
        name: String
        email: String
        address: String
        company: String
        posts: [Post]
    }

    type Query {
        users(limit: Int): [User]
        user(id: ID!): User
    }
""")

query = QueryType()
user_type = ObjectType("User")

@query.field("users")
def resolve_users(*_, limit=None):
    if limit:
        return db['users'][:limit]
    return db['users']

@query.field("user")
def resolve_user(*_, id):
    # Converte para string para garantir comparação correta
    return next((u for u in db['users'] if str(u['id']) == str(id)), None)

@user_type.field("posts")
def resolve_posts(user_obj, *_):
    return [p for p in db['posts'] if str(p['user_id']) == str(user_obj['id'])]

schema = make_executable_schema(type_defs, query, user_type)
app = Flask(__name__)

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

if __name__ == '__main__':
    print("Python GraphQL rodando na porta 5001...")
    app.run(port=5001, debug=False)