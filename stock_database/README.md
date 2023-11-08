# Database Desigg
## ERD
original data have two ways of representing, listed below, we are using the one with only 3 entities as this course does is focused on designing the system.
![ERD](./res/stock.drawio.png "database ERD")

## Data Cleaning
1. data_preprocessing.ipynb is the jupyter notebook file to perform data cleaning on aapl.csv file
2. data_preprocessing.py is the python script to processing other data and append to the transactions.csv

## docker compose
we plan to use postgreSQL database, "docker" folder contains the docker-comose configuration to setup database automatically

Requirements: \
1.docker enviroment
2.docker-compose

Steps: \
1. enter the docker folder, `cd docker`
2. run command `docker-compose up`
3. wait for the container to boot up and then **using `docker inspect -f '{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}' stocks` to get the IP address of the database container**
4. using pgAdmin (paramaters as follow) to connect to the database
![database container](./res/server_parameter.png "pgAdmin paramater")
![pgAdmin](./res/pgAdmin.png "pgAdmin")
4. example of using psycopg2 to connect to the database, code save to example_psycopg2.py
```python
db_url = "postgresql://postgres:postgres@172.25.0.1:6543/stocks"

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
```
4. using `docker-compose down` to clean the container created

## Create and Deploy database server
### Local Deploy and Test
**Database access without message queue**
1. database_client.py file directly invoke the database execution function
```bash
# start database service server
python database_server.py

# start client program to test and print result
python database_client.py

# result like this:
(SOA) ➜  database_server_deploy git:(dev-database) ✗ python database_client.py
POST request was successful!
{'transaction_id': 0, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 15869000, 'price': 3450000, 'size': 100, 'sale_condition_codes': '@F', 'suspicious': False}
{'transaction_id': 1, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 15870000, 'price': 3450100, 'size': 100, 'sale_condition_codes': '@F', 'suspicious': False}
{'transaction_id': 2, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 16768000, 'price': 3453400, 'size': 100, 'sale_condition_codes': '@F', 'suspicious': False}
{'transaction_id': 3, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 20357000, 'price': 3455000, 'size': 100, 'sale_condition_codes': '@F', 'suspicious': False}
{'transaction_id': 4, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 20764000, 'price': 3460000, 'size': 100, 'sale_condition_codes': 'T', 'suspicious': False}
{'transaction_id': 5, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 20855000, 'price': 3465000, 'size': 100, 'sale_condition_codes': 'T', 'suspicious': False}
{'transaction_id': 6, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 21546000, 'price': 3458000, 'size': 100, 'sale_condition_codes': '@F', 'suspicious': False}
{'transaction_id': 7, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 21551000, 'price': 3458000, 'size': 200, 'sale_condition_codes': 'T', 'suspicious': False}
{'transaction_id': 8, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 21904000, 'price': 3463700, 'size': 100, 'sale_condition_codes': 'T', 'suspicious': False}
{'transaction_id': 9, 'stock_id': 1, 'exchange_id': 'P', 'day': 1294876800000, 'time_of_the_day': 22024000, 'price': 3463700, 'size': 400, 'sale_condition_codes': 'T', 'suspicious': False}
```

