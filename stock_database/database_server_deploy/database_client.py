import requests
from sqlalchemy import text
import json

# Set the base URLs for the services this should be replaced query fromt the registry
db_service_url = 'http://localhost:5004'

# test program for the database_query
def example_query():
    sql_query = text("SELECT * FROM stock.\"Transactions\" ORDER BY transaction_id ASC LIMIT 10")
    data = {
        "sql_query": str(sql_query)
    }
    data_json = json.dumps(data)
    url = db_service_url + "/database/query"  # this should be replace by registry query result

    # Set the Content-Type header to specify JSON data
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data_json, headers=headers)
    # Check the response from the server

    if response.status_code == 200:
        print('POST request was successful!')
        # before usage, the json string need to be convert to json object
        result_text = response.text
        result_json = json.loads(result_text)
        for row in result_json:
            print(row)
    else:
        print('POST request failed with status code:', response.status_code)

def example_query_async():
    sql_query = text("SELECT * FROM stock.\"Transactions\" ORDER BY transaction_id ASC LIMIT 10")
    data = {
        "sql_query": str(sql_query)
    }
    data_json = json.dumps(data)
    url = db_service_url + "/database/query_async"  # this should be replace by registry query result

    # Set the Content-Type header to specify JSON data
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data_json, headers=headers)
    # Check the response from the server

    if response.status_code == 200:
        print('POST request was successful!')
        # before usage, the json string need to be convert to json object
        result_text = response.text
        result_json = json.loads(result_text)
        for row in result_json:
            print(row)
    else:
        print('POST request failed with status code:', response.status_code)

if __name__ == "__main__":
    # example_query()
    # below query is the example using cerey and redis invoking interafce async
    example_query_async()