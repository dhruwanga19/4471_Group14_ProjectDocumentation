
-- Create Schema stock
CREATE SCHEMA IF NOT EXISTS stock;

-- Name: Stocks; Type: TABLE; Schema:stock 
CREATE TABLE stock."Stocks" (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255)
);

-- Name: Exchanges; Type: TABLE; Schema:stock 
CREATE TABLE stock."Exchanges" (
    id VARCHAR(25) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Name: Transactions; Type: TABLE; Schema:stock 
CREATE TABLE stock."Transactions" (
    transaction_id INT NOT NULL PRIMARY KEY,
    stock_id INT NOT NULL,
    exchange_id VARCHAR(25) NOT NULL,
    day date NOT NULL,
    time_of_the_day INT NOT NULL,
    price INT NOT NULL,
    size INT NOT NULL,
    sale_condition_codes VARCHAR(4),
    suspicious boolean,
    FOREIGN KEY (stock_id) REFERENCES stock."Stocks" (id) ON DELETE CASCADE,
    FOREIGN KEY (exchange_id) REFERENCES stock."Exchanges" (id) ON DELETE CASCADE
);

-- Load data from csv files
COPY stock."Stocks" FROM '/csv/stocks.csv' 
DELIMITER ',' -- Fields in the CSV are separated by commas
CSV HEADER;   -- Specifies that the first row of the CSV contains column headers

COPY stock."Exchanges" FROM '/csv/exchanges.csv' 
DELIMITER ',' -- Fields in the CSV are separated by commas
CSV HEADER;   -- Specifies that the first row of the CSV contains column headers

COPY stock."Transactions" FROM '/csv/transactions.csv' 
DELIMITER ',' -- Fields in the CSV are separated by commas
CSV HEADER;   -- Specifies that the first row of the CSV contains column headers
