from flask import Flask, request, jsonify
import requests
import threading
import time


app = Flask(__name__)

# In-memory registry to store service information
service_registry = {}

@app.route('/register', methods=['POST'])
def register_service():
    data = request.json
    service_name = data['service_name']
    ip_address = data['ip_address']
    service_registry[service_name] = ip_address
    return jsonify({'message': 'Service registered successfully'}), 201

@app.route('/lookup/<service_name>', methods=['GET'])
def lookup_service(service_name):
    ip_address = service_registry.get(service_name, None)
    if ip_address is None:
        return jsonify({'message': 'Service not found'}), 404
    return jsonify({'ip_address': ip_address}), 200

@app.route('/deregister/<service_name>', methods=['DELETE'])
def deregister_service(service_name):
    if service_name in service_registry:
        del service_registry[service_name]
        return jsonify({'message': 'Service deregistered successfully'}), 200
    return jsonify({'message': 'Service not found'}), 404

@app.route('/bulk_health_check', methods=['GET'])
def bulk_health_check():
    unhealthy_services = []
    for service, ip_address in service_registry.items():
        url = f'http://{ip_address}/health'
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                unhealthy_services.append(service)
        except requests.RequestException:
            unhealthy_services.append(service)
    
    # Remove unhealthy services from registry
    for service in unhealthy_services:
        del service_registry[service]
    
    return jsonify({'unhealthy_services': unhealthy_services, 'updated_registry': service_registry})

# Function to perform health checks and update registry
def perform_health_checks():
    while True:
        unhealthy_services = []
        for service, ip_address in service_registry.items():
            url = f'http://{ip_address}/health'
            try:
                response = requests.get(url, timeout=5)
                if response.status_code != 200:
                    unhealthy_services.append(service)
            except requests.RequestException:
                unhealthy_services.append(service)
        
        # Remove unhealthy services from registry
        for service in unhealthy_services:
            del service_registry[service]
        
        print(f'Unhealthy services removed: {unhealthy_services}')
        print(f'Updated registry: {service_registry}')
        time.sleep(3)

# Start the health check thread
health_check_thread = threading.Thread(target=perform_health_checks)
health_check_thread.start()

if __name__ == '__main__':
    app.run(debug=True)