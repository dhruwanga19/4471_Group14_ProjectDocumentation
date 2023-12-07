-- Create schema for the registry
CREATE SCHEMA IF NOT EXISTS service_registry_schema;

-- Switch to the created schema
SET search_path TO service_registry_schema;

-- Create services table
CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL,
    service_description TEXT,
    service_url VARCHAR(255) NOT NULL,
    service_type VARCHAR(50) NOT NULL
);

-- Create providers table
CREATE TABLE providers (
    provider_id SERIAL PRIMARY KEY,
    provider_name VARCHAR(255) NOT NULL,
    service_id INT REFERENCES services(service_id) ON DELETE CASCADE,
    provider_ip VARCHAR(15) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    heartbeat_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create registry servers table
CREATE TABLE registry_servers (
    server_id SERIAL PRIMARY KEY,
    server_name VARCHAR(255) NOT NULL,
    server_ip VARCHAR(15) NOT NULL,
    is_backup BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create a table to associate registry servers with services
CREATE TABLE service_registry_servers (
    service_id INT REFERENCES services(service_id) ON DELETE CASCADE,
    server_id INT REFERENCES registry_servers(server_id) ON DELETE CASCADE,
    PRIMARY KEY (service_id, server_id)
);

-- -- Sample data
-- INSERT INTO services (service_name, service_description, service_url, service_type)
-- VALUES
--     ('Service101', 'Provide Overall stock performance', 'http://127.0.0.1:5011', 'REST'),
--     ('Service102', 'Handle User Authentication', 'http://127.0.0.1:5012', 'REST');
-- 
-- INSERT INTO providers (provider_name, service_id, provider_ip)
-- VALUES
--     ('ProviderA', 1, '192.168.0.1'),
--     ('ProviderB', 1, '192.168.0.2'),
--     ('ProviderC', 2, '192.168.0.3');
-- 
-- INSERT INTO registry_servers (server_name, server_ip, is_backup)
-- VALUES
--     ('PrimaryRegistry', '192.168.1.1', FALSE),
--     ('BackupRegistry', '192.168.1.2', TRUE);
-- 
-- INSERT INTO service_registry_servers (service_id, server_id)
-- VALUES
--     (1, 1),  -- Service101 is registered in the PrimaryRegistry
--     (2, 1);  -- Service102 is registered in the PrimaryRegistry
