from flask import Flask, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from flask_cors import CORS
import numpy as np
import io
import base64
import json
import requests
import schedule
import pandas as pd
import time

app = Flask(__name__)
CORS(app)

# Registry server endpoint for service registration
PORT = 5012  # Change the port for the new service
REGISTRY_SERVER_IP = "http://54.174.175.123"
REGISTRY_SERVICES = REGISTRY_SERVER_IP + ":8511"
REGISTRY_SERVICES_API_URL = REGISTRY_SERVICES + "/services"
REGISTRY_REGISTER_API_URL = REGISTRY_SERVICES + "/register"
REGISTRY_PROVIDER_API_URL = REGISTRY_SERVICES + "/register/provider"
REGISTRY_HEARTBEAT_API_URL = REGISTRY_SERVICES + "/heartbeat"

PROVIDER_SERVER_IP = "http://34.201.71.7"
PROVIDER_IP = PROVIDER_SERVER_IP + ":8502"  # Change the provider IP for the new service

# Register the service
def register_service():
    service_data = {
        "service_name": "Service102",  # StockNotifications
        "service_description": "Service that provides stock notifications",
        "service_url": PROVIDER_IP,
        "service_type": "REST"
    }

    response = requests.post(REGISTRY_REGISTER_API_URL, json=service_data)

    if response.status_code == 201:
        print('Service registered successfully!')
    else:
        print('Failed to register service with status code:', response.status_code)


def send_heartbeat():
    heartbeat_data = {
        "provider_name": "StockNotificationsProvider",
        "service_name": "Service102"  # Replace with the actual service name
    }
    response = requests.post(REGISTRY_HEARTBEAT_API_URL, json=heartbeat_data)

    if response.status_code == 200:
        print('Heartbeat sent successfully!')
    else:
        print('Failed to send heartbeat with status code:', response.status_code)


# Register the service provider
def register_service_provider():
    service_name = "Service102"  # Change the service name for the new service

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
            "provider_name": "StockNotificationsProvider",  # Change the provider name for the new service
            "service_name": service_name,
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

# Endpoint to handle subscription requests
@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.json
        # Handle the subscription logic here
        # You can access the data using data['stockName'], data['parameter'], and data['email']

        # Example subscription logic - replace with your actual logic
        if 'stockName' not in data or 'parameter' not in data or 'email' not in data:
            raise ValueError("Missing required data in the request")

        subscription_status = f"Subscribed to {data['stockName']} notifications for {data['parameter']} parameter."
        print(subscription_status)

        # Return a response (replace with your actual response)
        return jsonify({'message': subscription_status})

    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error during subscription: {str(e)}")
        return jsonify({'error': str(e)}), 500  # Return a 500 Internal Server Error status

# Endpoint to check the status of the provider
@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Provider is running', 'provider_name': 'Service102'})

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

