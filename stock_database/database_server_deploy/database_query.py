import pandas as pd
from sqlalchemy import create_engine, text
import json

# load database configuration from json file
def get_db_config():
    with open('database_configuration.json', 'r') as file:
        # load json file to config
        config = json.load(file)
        return config

# receive a json string contains query_sql
def execute_database_operation(data_json_string):
    try:
        db_config = get_db_config()
        user = db_config["user"]
        password = db_config["password"]
        database = db_config["database"]
        ip = db_config["ip"]
        port = db_config["port"]
        db_url = f"postgresql://{user}:{password}@{ip}:{port}/{database}"

        # print the parameters for debug
        # print(f"User: {user}")
        # print(f"Password: {password}")
        # print(f"Database: {database}")
        # print(f"IP: {ip}")
        # print(f"Port: {port}")

        # Create a SQLAlchemy engine
        engine = create_engine(db_url)
        # Establish a connection to the database
        conn = engine.connect()

        # Convert the json string into json object
        data = json.loads(data_json_string)
        sql_query = text(data["sql_query"])

        df = pd.read_sql(sql_query, engine)
        df_json = df.to_json(orient='records')

        # Close the database connection
        conn.close()

        return df_json
    except Exception as e:
        # Handle the exception and return an error message as a JSON string
        error_message = {"error": str(e)}
        return json.dumps(error_message)
        

if __name__ == '__main__':
    # test function functionality
    query = {
        "sql_query": str(text("SELECT * FROM stock.\"Transactions\" ORDER BY transaction_id ASC LIMIT 10"))
    }
    query_json = json.dumps(query)
    result  = execute_database_operation(query_json)
    result_json = json.loads(result)
    print(result_json)