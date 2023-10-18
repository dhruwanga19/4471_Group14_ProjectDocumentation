from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = len(users) + 1
    users[user_id] = data
    return jsonify({"user_id": user_id}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        return "User not found", 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True, port=5000)