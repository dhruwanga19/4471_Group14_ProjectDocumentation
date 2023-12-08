from flask import Flask, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from flask_cors import CORS
import numpy as np
import io
import base64
from sqlalchemy import text
import json
import requests
import schedule
import pandas as pd
import time

app = Flask(__name__)
CORS(app)

# Registry server endpoint for service registration
PORT = 5011
REGISTRY_SERVER_IP = "http://54.174.175.123"
REGISTRY_SERVICES = REGISTRY_SERVER_IP + ":8511"
REGISTRY_SERVICES_API_URL = REGISTRY_SERVICES + "/services"
REGISTRY_REGISTER_API_URL = REGISTRY_SERVICES + "/register"
REGISTRY_PROVIDER_API_URL = REGISTRY_SERVICES + "/register/provider"
REGISTRY_HEARTBEAT_API_URL = REGISTRY_SERVICES + "/heartbeat"

PROVIDER_SERVER_IP = "http://34.201.71.7"
PROVIDER_IP = PROVIDER_SERVER_IP + ":8501"

# Fake data
x = np.linspace(0, 10, 100)
y = np.sin(x)

def generate_plot(df):
    # fetch data from database server
    # currently using fake data
    df['time_of_the_day_seconds'] = df['time_of_the_day'].dt.total_seconds()

    # generate plot image
    plt.figure(figsize=(12, 6))

    # price left y axis
    plt.plot(df['time_of_the_day_seconds'], df['price'], color='blue', marker='o', label='Price')
    plt.xlabel('Second of the Day')
    plt.ylabel('Price')

    ax2 = plt.twinx()
    ax2.bar(df['time_of_the_day_seconds'], df['size'], color='green', label='Size')
    ax2.set_ylabel('Size')

    # Set the desired limits for the y-axis of the 'size' bar plot
    ax2.set_ylim(0, max(df['size']))  # You can adjust the limits as needed

    plt.title('Price and Size vs Time of the Day')
    ax2.legend(loc='upper right')

    # save the image to ram and sent via http request
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # conver the imge_buffer to base64 encoding
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

    plt.clf()

    return img_base64

def query_transaction_data(stock_name, start_date, end_date):
    # Parameters for the SQL query
    # start_date_int = pd.to_datetime(start_date).timestamp() * 1000
    # end_date_int = pd.to_datetime(end_date).timestamp() * 1000
    # Parameters for the SQL query
    # Adjust the SQL query based on your database schema
    sql_query = text(f"""
        SELECT *
        FROM stock."Transactions"
        WHERE stock_id = (SELECT id FROM stock."Stocks" WHERE name = '{stock_name}')
          AND day + (time_of_the_day * INTERVAL '1 millisecond') BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY transaction_id ASC
        LIMIT 1000
    """)

    data = {
        "sql_query": str(sql_query),
    }
    data_json = json.dumps(data)

    db_service_url = "http://54.174.175.123:8504"
    url = db_service_url + "/database/query"  # This should be replaced by registry query result

    # Set the Content-Type header to specify JSON data
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data_json, headers=headers)

    if response.status_code == 200:
        print('POST request was successful!')
        # Before usage, the JSON string needs to be converted to a JSON object
        result_text = response.text
        result_json = json.loads(result_text)
        df = pd.DataFrame(result_json)
        df['time_of_the_day'] = pd.to_timedelta(df['time_of_the_day'], unit='ms')
        print("finsihed!")

        return df
    else:
        print('POST request failed with status code:', response.status_code)
        return None

def register_service():
    service_data = {
        "service_name": "Service101",
        "service_description": "Service that provides stock plots",
        "service_url": PROVIDER_IP,  # Update this URL based on your service's address
        "service_type": "REST"
    }

    response = requests.post(REGISTRY_REGISTER_API_URL, json=service_data)

    if response.status_code == 201:
        print('Service registered successfully!')
    else:
        print('Failed to register service with status code:', response.status_code)

def send_heartbeat():
    heartbeat_data = {
        "provider_name": "StockPlotProvider",
        "service_name": "Service101"  # Replace with the actual service name
    }
    response = requests.post(REGISTRY_HEARTBEAT_API_URL, json=heartbeat_data)

    if response.status_code == 200:
        print('Heartbeat sent successfully!')
    else:
        print('Failed to send heartbeat with status code:', response.status_code)

# Register the service provider
def register_service_provider():
    service_name = "Service101"  # Replace with the actual service name

    # Check if the service exists
    response = requests.get(REGISTRY_SERVICES_API_URL)
    if response.status_code == 200:
        data = response.json()
        services = data.get('services')

        # Check if the service with the specified name exists
        existing_service = next((service for service in services if service['service_name'] == service_name), None)

        if existing_service:
            print('Service already exists. Skipping Service registration.')
        else:
            # Register the service
            register_service()
            print('Service not found. Registering the service.')

        # Now register the service provider
        provider_data = {
            "provider_name": "StockPlotProvider",
            "service_name": service_name,  # Replace with the actual service_id from the registry
            "provider_ip": PROVIDER_IP
        }

        response = requests.post(REGISTRY_PROVIDER_API_URL, json=provider_data)

        if response.status_code == 201:
            print('Service provider registered successfully!')
        else:
            print('Failed to register service provider with status code:', response.status_code)

# Uncomment the line below to register the service when the script is run
register_service_provider()

# Schedule heartbeat without entering an infinite loop
schedule.every(4).seconds.do(send_heartbeat)

@app.route('/get_stock_plot', methods=['POST'])
def get_stock_plot():
    try:
        # Get JSON data, which contains stock name, time frame
        json_data = request.json

        # Extract stock name and time frame from the JSON data
        stock_name = json_data.get('stock_name')
        start_date = json_data.get('start_date')
        end_date = json_data.get('end_date')

        # Query transaction data based on input values
        df = query_transaction_data(stock_name, start_date, end_date)

        if df is not None:
            # Generate plot
            img_base64 = generate_plot(df)

            return jsonify({'image': img_base64})
        else:
            return jsonify({'error': 'No data found for the specified parameters.'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to check the status of the provider
@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Provider is running', 'provider_name': 'Service101'})

if __name__ == '__main__':
    import threading

    # Define a function to run the scheduler in a separate thread
    def schedule_thread():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Start the scheduler thread
    scheduler_thread = threading.Thread(target=schedule_thread)
    scheduler_thread.start()

    # Run the Flask app
    app.run(debug=True, port=PORT)
