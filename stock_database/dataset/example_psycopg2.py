import pandas as pd
import psycopg2 # for PostgreSQL connection
from sqlalchemy import create_engine, text

if __name__ == '__main__':
    # Define your PostgreSQL database connection URL
    user = "postgres"
    passward = "postgres"
    database = "stocks"
    ip = "172.25.0.1:6543"
    db_url = "postgresql://" + user + ":" + passward + "@" + ip + "/" + database
    #db_url = "postgresql://postgres:postgres@172.25.0.1:6543/stocks"

    # Create a SQLAlchemy engine
    engine = create_engine(db_url)
    # Establish a connection to the database
    conn = engine.connect()

    # Write your SQL query to retrieve the first 100 rows from the 'Transactions' table
    # SELECT * FROM stock."Transactions"
    # ORDER BY transaction_id ASC LIMIT 100
    sql_query = text("SELECT * FROM stock.\"Transactions\" ORDER BY transaction_id ASC LIMIT 100")

    # Execute the query and fetch the results into a DataFrame
    result = conn.execute(sql_query)
    data = result.fetchall()
    print(data)
    df = pd.DataFrame(data, columns=result.keys())

    # Close the database connection
    conn.close()
