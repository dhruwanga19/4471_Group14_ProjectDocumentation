import requests

# Set the base URLs for the services
user_service_url = 'http://18.234.215.48:8500'  # Replace with the actual URL of your User Service
product_service_url = 'http://18.234.215.48:8501'  # Replace with the actual URL of your Product Service

# Helper function to create a user
def create_user(user_data):
    response = requests.post(f'{user_service_url}/users', json=user_data)
    return response.json()

# Helper function to get a user by ID
def get_user(user_id):
    response = requests.get(f'{user_service_url}/users/{user_id}')
    return response.json()

# Helper function to create a product
def create_product(product_data):
    response = requests.post(f'{product_service_url}/products', json=product_data)
    return response.json()

# Helper function to get a product by ID
def get_product(product_id):
    response = requests.get(f'{product_service_url}/products/{product_id}')
    return response.json()

if __name__ == '__main__':
    print("start!")
    # Create a user
    user_data = {'username': 'john_doe', 'email': 'john@example.com'}
    created_user = create_user(user_data)
    print('Created User:', created_user)

    # Get the user by ID
    user_id = created_user['user_id']
    retrieved_user = get_user(user_id)
    print('Retrieved User:', retrieved_user)

    # Create a product
    product_data = {'name': 'Example Product', 'price': 19.99}
    created_product = create_product(product_data)
    print('Created Product:', created_product)

    # Get the product by ID
    product_id = created_product['product_id']
    retrieved_product = get_product(product_id)
    print('Retrieved Product:', retrieved_product)
