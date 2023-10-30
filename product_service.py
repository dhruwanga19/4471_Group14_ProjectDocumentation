from flask import Flask, request, jsonify

app = Flask(__name__)

products = {}

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product_id = len(products) + 1
    products[product_id] = data
    return jsonify({"product_id": product_id}), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product is None:
        return "Product not found", 404
    return jsonify(product)

if __name__ == '__main__':
    app.run(debug=True, port=5001)