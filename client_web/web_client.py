from flask import Flask, render_template, request
import requests

DEFAULT_PORT = 5005

app = Flask(__name__)

# Registry server endpoint for services
SERVER_IP = "http://54.174.175.123"
REGISTRY_API_URL = SERVER_IP + ":8511/services"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')

    # Fetch services from the registry server
    response = requests.get(REGISTRY_API_URL)

    if response.status_code == 200:
        data = response.json()

        # Filter services based on the keyword
        filtered_services = filter_services(data.get('services'), keyword)

        return render_template('search_results.html', results=filtered_services)
    else:
        return "Error fetching data from the registry server!"

# Function to filter services based on the keyword
def filter_services(services, keyword):
    filtered_services = []
    for service in services:
        # Check if the lowercase keyword is in any of the lowercase service attributes
        if keyword.lower() in service['service_name'].lower() or \
           keyword.lower() in service['service_description'].lower() or \
           keyword.lower() in service['service_type'].lower():
            filtered_services.append(service)
    return filtered_services

@app.route('/service_display/<string:service_name>')
def service_display(service_name):
    # Fetch services from the registry server
    response = requests.get(REGISTRY_API_URL)

    if response.status_code == 200:
        data = response.json()
        services = data.get('services')
        
        # Find the service with the specified service_name
        selected_service = next((service for service in services if service['service_name'] == service_name), None)
        
        if selected_service:
            # You can modify this to handle different subpage URLs based on service attributes
            subpage_url = selected_service.get('service_name', None) + ".html"
            if subpage_url:
                return render_template(subpage_url)
            else:
                return f"Subpage for service: {service_name} not found!"
        else:
            return f"Service with name {service_name} not found!"
    else:
        return "Error fetching data from the registry server!"


if __name__ == '__main__':
    app.run(debug=True, port=DEFAULT_PORT)
