from flask import Flask, jsonify
from ariadne import gql, QueryType, make_executable_schema
from ariadne.contrib.flask import GraphQL

COMMENTS_DATA = [
    {"id": "1", "userId": "13", "score": 3, "text": "This is okay."},
    {"id": "2", "userId": "10", "score": 8, "text": "Amazing!"},
    {"id": "3", "userId": "13", "score": 9, "text": "My favorite one."},
    {"id": "4", "userId": "11", "score": 5, "text": "Not bad."},
    {"id": "5", "userId": "10", "score": 1, "text": "Terrible."},
]

app = Flask(__name__)

@app.route('/rest/comments', methods=['GET'])
def rest_all_comments():
    return jsonify(COMMENTS_DATA)

@app.route('/rest/comments/<string:id>', methods=['GET'])
def rest_comment_by_id(id):
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
GraphQL(app, schema, debug=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)