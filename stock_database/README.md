# Database Design
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
#### Database access without message queue
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
#### Database access using message queue
**Redis configuration**
```bash
# instll the redis first
sudo apt update
sudo apt install redis-server

# configuration
sudo vim /etc/redis/redis.conf
sudo systemctl restart redis-server
sudo systemctl status redis-server

# connect to the redis server
redis-cli

# python enviroment
pip install celery
pip install redis
```
**Example setup of the redis-server**
```bash
# Network address and port to listen on
bind 127.0.0.1
port 6379

# Password authentication
# requirepass your_password

# Log file
logfile /var/log/redis/redis-server.log

# Database file storage directory
dir /var/lib/redis

# Maximum memory limit
# maxmemory 2GB

# Data persistence options
save 900 1
save 300 10
save 60 10000

# RDB persistence snapshot file name
dbfilename dump.rdb

# AOF persistence options
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# Set the maximum number of clients
maxclients 10000

# Disable protected mode (by default, only local connections are allowed)
# protected-mode no

# Limit maximum query time for clients (0 means no limit)
timeout 300

# Run Redis in the background
daemonize yes
```
**Code example processdure**
1. running command `celery -A database_queue worker --loglevel=info` start celery worker for task processing
2. running database server instance `python database_server.py`
3. running client program, invoke async query `python database_client.py`

**celery log**
```bash
(SOA) ➜  database_server_deploy git:(dev-database) ✗ celery -A database_queue worker --loglevel=info
 
 -------------- celery@clay-ThinkBook-14 v5.3.4 (emerald-rush)
--- ***** ----- 
-- ******* ---- Linux-5.15.0-86-generic-x86_64-with-glibc2.17 2023-11-07 22:42:16
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         database_queue:0x7f13c227c4f0
- ** ---------- .> transport:   redis://localhost:6379/0
- ** ---------- .> results:     redis://localhost:6379/1
- *** --- * --- .> concurrency: 12 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . database_queue.process_message

[2023-11-07 22:42:17,481: WARNING/MainProcess] /home/clay/anaconda3/envs/SOA/lib/python3.8/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
whether broker connection retries are made during startup in Celery 6.0 and above.
If you wish to retain the existing behavior for retrying connections on startup,
you should set broker_connection_retry_on_startup to True.
  warnings.warn(

[2023-11-07 22:42:17,498: INFO/MainProcess] Connected to redis://localhost:6379/0
[2023-11-07 22:42:17,500: WARNING/MainProcess] /home/clay/anaconda3/envs/SOA/lib/python3.8/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
whether broker connection retries are made during startup in Celery 6.0 and above.
If you wish to retain the existing behavior for retrying connections on startup,
you should set broker_connection_retry_on_startup to True.
  warnings.warn(

[2023-11-07 22:42:17,503: INFO/MainProcess] mingle: searching for neighbors
[2023-11-07 22:42:18,513: INFO/MainProcess] mingle: all alone
[2023-11-07 22:42:18,532: INFO/MainProcess] celery@clay-ThinkBook-14 ready.
[2023-11-07 22:42:18,736: INFO/MainProcess] Task database_queue.process_message[4e464e87-1ed2-455c-adbd-fb82eb3659f5] received
[2023-11-07 22:42:18,827: INFO/ForkPoolWorker-8] Task database_queue.process_message[4e464e87-1ed2-455c-adbd-fb82eb3659f5] succeeded in 0.08914547204039991s: '[{"transaction_id":0,"stock_id":1,"exchange_id":"P","day":1294876800000,"time_of_the_day":15869000,"price":3450000,"size":100,"sale_condition_codes":"@F","suspicious":false},{"transaction_id":1,"stock_id":1,"exchange_id":"P","day":1294876800000,"time_of_the_day":15870000,"price":3450100,"size":100,"sale_condition_codes":"@F","suspicious":false},{"transaction_id":2,"stock_id":1,"exchange_id":"P","day":1294876800000,"time_of_the_day":16768000,"price":3453400,"size":100,"sale_condition_codes":"@F","suspicious":false},{"transaction_id":3,"stock_id":1,"exchange_id":"P","day":1294876800000,"time_of_the_day":20357000,"price":3455000,"size":100,"sale_condition_codes":"@F","suspicious":false},{"transaction_id":4,"stock_id":1,"exchange_id":"P","day":1294876800000,"time_of_the_day":20764000,"price":3460000,"size":100,"sale_condition_codes":"T","suspicious":false},{"transaction_id":5,"stock_id":1,"exchange_id":"P","day":1294876800000,"time_of_the_day":20855000,"price":3465000,"size":100,"sale_condition_codes":"T","suspic...'
^C
worker: Hitting Ctrl+C again will terminate all running tasks!

worker: Warm shutdown (MainProcess)

```
**client result**
```bash
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
