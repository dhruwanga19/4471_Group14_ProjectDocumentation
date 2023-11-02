# Database Desigg
## ERD
original data have two ways of representing, listed below, we are using the one with only 3 entities as this course does is focused on designing the system.
![ERD](./stock.drawio.png "database ERD")

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
![database container](./server_parameter.png "pgAdmin paramater")
![pgAdmin](./pgAdmin.png "pgAdmin")
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
