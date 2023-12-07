from flask import Flask, request, jsonify
from database_query import execute_database_operation
from database_queue import process_message
app = Flask(__name__)

@app.route('/database/query', methods=['POST'])
def handle_query():
    # process the client request, execute the database query
    data = request.json  # get request from client
    # execute the database query
    result = execute_database_operation(data)
    return result

@app.route('/database/query_async', methods=['POST'])
def handler_query_async():
    data = request.json
    result = process_message.delay(data)
    return result.get()

if __name__ == '__main__':
    app.run(debug=True, port=5004)
