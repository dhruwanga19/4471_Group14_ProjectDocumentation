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
3. wait for the container to boot up and then using pgAdmin (paramaters as follow) or psycopg2 lib
![database container](./server_parameter.png "pgAdmin paramater")
4. using `docker-compose down` to clean the container created

