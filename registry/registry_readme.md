# registry documentation

## versions
1. base registry with POST, GET, and DELETE. No health check, no persistent database
2. updated with automatic health check and bulk health check
3. WIP working on potential persistent database

## running and testing
1. install flask and any other packages needed
```bash
pip install Flask
```

2. running the service_registry
```bash
python service_registry.py
```
without config, the registry will be default accessible at http://127.0.0.1:5000/

3. testing POST, GET, and DELETE
```bash
curl -X POST -H "Content-Type: application/json" -d '{"service_name": "service_one", "ip_address": "111.111.1.1"}' http://127.0.0.1:5000/register
curl http://127.0.0.1:5000/lookup/service_one
curl -X DELETE http://127.0.0.1:5000/deregister/service_one
```
we assume unique service's name, adding double checking sys later

use '/bulk_health_check' to check if automatic health checking functions 
```bash
curl http://127.0.0.1:5000/bulk_health_check
```

## use cases
![registry use case](registry/registry_use_case_1.pdf "registry use case")

