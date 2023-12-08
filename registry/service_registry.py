from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from flask_cors import CORS  # Import the CORS module

DEFAULT_PORT = 5111

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Read database configuration from config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = config_data.get('DATABASE_URL', '')
db = SQLAlchemy(app)

class Service(db.Model):
    __tablename__ = 'services'
    __table_args__ = {'schema': 'service_registry_schema'}
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(255), nullable=False)
    service_description = db.Column(db.Text)
    service_url = db.Column(db.String(255), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    providers = db.relationship('Provider', back_populates='service')

class Provider(db.Model):
    __tablename__ = 'providers'
    __table_args__ = {'schema': 'service_registry_schema'}
    provider_id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(255), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service_registry_schema.services.service_id', ondelete='CASCADE'), nullable=False)
    provider_ip = db.Column(db.String(15), nullable=False)
    registration_date = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    heartbeat_timestamp = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    service = db.relationship('Service', back_populates='providers')

class RegistryServer(db.Model):
    __tablename__ = 'registry_servers'
    __table_args__ = {'schema': 'service_registry_schema'}
    server_id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(255), nullable=False)
    server_ip = db.Column(db.String(15), nullable=False)
    is_backup = db.Column(db.Boolean, nullable=False, default=False)

class ServiceRegistryServer(db.Model):
    __tablename__ = 'service_registry_servers'
    __table_args__ = {'schema': 'service_registry_schema'}
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id', ondelete='CASCADE'), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey('registry_servers.server_id', ondelete='CASCADE'), nullable=False, primary_key=True)

# Flask routes
@app.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    service_list = []
    for service in services:
        service_list.append({
            'service_id': service.service_id,
            'service_name': service.service_name,
            'service_description': service.service_description,
            'service_url': service.service_url,
            'service_type': service.service_type
        })
    return jsonify({'services': service_list})

@app.route('/register', methods=['POST'])
def register_service():
    data = request.get_json()
    service_name = data.get('service_name')
    service_description = data.get('service_description')
    service_url = data.get('service_url')
    service_type = data.get('service_type')

    # Validate input
    if not service_name or not service_url or not service_type:
        return jsonify({'error': 'Incomplete data'}), 400

    # Create a new service
    new_service = Service(
        service_name=service_name,
        service_description=service_description,
        service_url=service_url,
        service_type=service_type
    )
    
    db.session.add(new_service)
    db.session.commit()

    return jsonify({'message': 'Service registered successfully'}), 201

@app.route('/register/provider', methods=['POST'])
def register_provider():
    data = request.get_json()
    provider_name = data.get('provider_name')
    service_name = data.get('service_name')  # Add service_name to provider registration
    provider_ip = data.get('provider_ip')

    # Validate input
    if not provider_name or not service_name or not provider_ip:
        return jsonify({'error': 'Incomplete data'}), 400

    # Check if the service_name exists
    existing_service = Service.query.filter_by(service_name=service_name).first()
    if not existing_service:
        return jsonify({'error': 'Service not found'}), 404

    # Check if the provider_name is already registered for the given service
    existing_provider = Provider.query.filter_by(provider_name=provider_name, service_id=existing_service.service_id).first()
    if existing_provider:
        return jsonify({'message': 'Provider already registered for this service'}), 200

    # Create a new provider
    new_provider = Provider(
        provider_name=provider_name,
        service_id=existing_service.service_id,
        provider_ip=provider_ip
    )

    db.session.add(new_provider)
    db.session.commit()

    return jsonify({'message': 'Provider registered successfully'}), 201

def cleanup_inactive_providers():
    with app.app_context():
        # Cleanup inactive providers (those that haven't sent heartbeats within the last 5 minutes)
        inactive_threshold = datetime.utcnow() - timedelta(seconds=2)
        inactive_providers = Provider.query.filter(Provider.heartbeat_timestamp < inactive_threshold).all()

        for provider in inactive_providers:
            db.session.delete(provider)

        # Get services with no providers
        services_with_no_providers = Service.query.filter(~Service.providers.any()).all()

        for service in services_with_no_providers:
            db.session.delete(service)

        db.session.commit()

# Configure Flask-APScheduler
class Config:
    JOBS = [
        {
            'id': 'heartbeat_cleanup',
            'func': cleanup_inactive_providers,
            'trigger': 'interval',
            'seconds': 2  # Adjust the interval as needed
        }
    ]

app.config.from_object(Config)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.get_json()
    provider_name = data.get('provider_name')
    service_name = data.get('service_name')

    if not provider_name or not service_name:
        return jsonify({'error': 'Incomplete data'}), 400

    existing_provider = Provider.query.join(Service).filter(Service.service_name == service_name, Provider.provider_name == provider_name).first()

    if not existing_provider:
        return jsonify({'error': 'Provider not found'}), 404

    existing_provider.heartbeat_timestamp = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Heartbeat received successfully'}), 200

@app.route('/get_providers/<service_name>', methods=['GET'])
def get_providers_for_service(service_name):
    # Find the service by name
    service = Service.query.filter_by(service_name=service_name).first()

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    # Get the providers for the service
    providers = Provider.query.filter_by(service_id=service.service_id).all()

    providers_list = [{
        'provider_name': provider.provider_name,
        'provider_ip': provider.provider_ip,
        'registration_date': provider.registration_date,
        'heartbeat_timestamp': provider.heartbeat_timestamp
    } for provider in providers]

    return jsonify({
        'service_name': service.service_name,
        'providers': providers_list
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=DEFAULT_PORT)
