import pandas as pd

# define data path
ori_path_prefix = "original_data/"
modified_path_prefix = "modified_data/"

def setup():
    # make the Stocks csv file
    stocks_data = {
        'id': [1, 2, 3],
        'name': ['aapl', 'intl', 'amd'],
        'company': ['apple', 'intel', 'amd']
    }
    
    stocks_df = pd.DataFrame(stocks_data)
    # save to stocks.csv
    stocks_df.to_csv(modified_path_prefix + 'stocks.csv', index=False)
    # make the Exchanges csv file
    exchanges_data = {
        'id': ['A', 'B', 'C', \
            'D', 'I', 'J', \
                'K', 'M', 'N', \
                    'T', 'P', 'S', \
                        'Q', 'W', 'X', \
                            'Y', 'Z'],
        'name': ['NYSE MKT Stock Exchange', 'NASDAQ OMX BX Stock Exchange', 'National Stock Exchange', \
            'FINRA', 'International Securities Exchange', 'Direct Edge A Stock Exchange', \
                'Direct Edge X Stock Exchange', 'Chicago Stock Exchange', 'New York Stock Exchange', \
                    'NASDAQ OMX Stock Exchange', 'NYSE Arca SM', 'Consolidated Tape System', \
                        'NASDAQ Stock Exchange', 'CBOE Stock Exchange', 'NASDAQ OMX PSX Stock Exchange', \
                            'BATS Y-Exchange', 'BATS Exchange']
    }
    
    exchanges_df = pd.DataFrame(exchanges_data)
    # save to stocks.csv
    exchanges_df.to_csv(modified_path_prefix + 'exchanges.csv', index=False)
    # read aapl.csv file
    aapl_df = pd.read_csv(ori_path_prefix + "aapl.csv")
    aapl_des = aapl_df.describe()
    # the original csv file contains no column headers, add headers
    aapl_df_headers = ['time_of_the_day', 'price', 'size','exchange_id', 'sale_condition_codes', 'suspicious']
    aapl_df.columns = aapl_df_headers
    # add stock_id column
    result = stocks_df.loc[stocks_df['name'] == 'aapl', 'id']
    if not result.empty:
        stock_id = result.iloc[0]
        print(stock_id)
    aapl_df['stock_id'] = stock_id
    
    # add transaction_id
    aapl_df.reset_index(inplace=True)
    aapl_df.rename(columns={'index': 'transaction_id'}, inplace=True)
    
    # add day column
    aapl_df['day'] = pd.to_datetime('2011-01-13')
    
    # rearrange and save to csv file
    aapl_df = aapl_df[['transaction_id', 'stock_id', 'exchange_id', 'day', 'time_of_the_day', 'price', 'size', 'sale_condition_codes', 'suspicious']]
    aapl_df.to_csv(modified_path_prefix + 'transactions.csv', index=False)

def get_data_frame(name, date):
    # read stocks.csv
    stocks_df = pd.read_csv(modified_path_prefix + 'stocks.csv')
    # read transactions.csv
    transaction_df = pd.read_csv(modified_path_prefix + 'transactions.csv')
    # read csv file
    df = pd.read_csv(ori_path_prefix + name +".csv")
  
    # the original csv file contains no column headers, add headers
    df_headers = ['time_of_the_day', 'price', 'size','exchange_id', 'sale_condition_codes', 'suspicious']
    df.columns = df_headers
    # add stock_id column
    result = stocks_df.loc[stocks_df['name'] == name, 'id']
    if not result.empty:
        stock_id = result.iloc[0]
        print(stock_id)
    else :
        print("error while processing stock_id!")
    df['stock_id'] = stock_id
  
    # add day column
    df['day'] = pd.to_datetime(date)
    # add date
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'transaction_id'}, inplace=True)
  
    # rearrange and save to csv file
    # df = df[['stock_id', 'exchange_id', 'day', 'time_of_the_day', 'price', 'size', 'sale_condition_codes', 'suspicious']]
    # transaction_df = transaction_df[['stock_id', 'exchange_id', 'day', 'time_of_the_day', 'price', 'size', 'sale_condition_codes', 'suspicious']]
    new_transaction_df = pd.concat([transaction_df, df], ignore_index=True)
    new_transaction_df = new_transaction_df[['stock_id', 'exchange_id', 'day', 'time_of_the_day', 'price', 'size', 'sale_condition_codes', 'suspicious']]
    new_transaction_df.reset_index(inplace=True)
    new_transaction_df.rename(columns={'index': 'transaction_id'}, inplace=True)
    new_transaction_df.to_csv(modified_path_prefix + 'transactions.csv', index=False)

if __name__ == "__main__":
    setup() # get_data_frame('aapl', '2011-01-13')
    get_data_frame('amd', '2011-01-13')
    get_data_frame('intl', '2011-01-13')