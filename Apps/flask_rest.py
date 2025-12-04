import json
from flask import Flask, jsonify

app = Flask(__name__)

# Carregar dados
with open('../Data/database_100k_user.json', 'r') as f:
    db = json.load(f)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(db['users'])

@app.route('/users/<int:user_id>/full', methods=['GET'])
def get_user_full(user_id):
    user = next((u for u in db['users'] if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "Not found"}), 404
    
    posts = [p for p in db['posts'] if p['user_id'] == user_id]
    response = user.copy()
    response['posts'] = posts
    return jsonify(response)

@app.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    posts = [p for p in db['posts'] if p['user_id'] == user_id]
    return jsonify(posts)

if __name__ == '__main__':
    app.run(port=5000, debug=False)