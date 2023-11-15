from flask import Flask, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from flask_cors import CORS
import numpy as np
import io
import base64
from sqlalchemy import text
import json
import requests
import pandas as pd

# Fake data
x = np.linspace(0, 10, 100)
y = np.sin(x)

app = Flask(__name__)
CORS(app)

def generate_plot(df):
    # fetch data from database server
    # currently using fake data
    df['time_of_the_day_seconds'] = df['time_of_the_day'].dt.total_seconds()

    # generate plot image
    plt.figure(figsize = (12, 6))

    # price left y axis
    plt.plot(df['time_of_the_day_seconds'], df['price'], color='blue', marker='o', label='Price')
    plt.xlabel('Second of the Day')
    plt.ylabel('Price')

    ax2 = plt.twinx()
    ax2.bar(df['time_of_the_day_seconds'], df['size'], color='green', label='Size')
    ax2.set_ylabel('Size')

    # Set the desired limits for the y-axis of the 'size' bar plot
    ax2.set_ylim(0, max(df['size']))  # You can adjust the limits as needed

    plt.title('Price and Size vs Time of the Day')
    ax2.legend(loc='upper right')

    # save the image to ram and sent via http request
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # conver the imge_buffer to base64 encoding
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

    plt.clf()

    return img_base64

# Set the base URLs for the services this should be replaced query fromt the registry
db_service_url = 'http://localhost:5004'

def query_transaction_data():
    sql_query = text("SELECT * FROM stock.\"Transactions\" ORDER BY transaction_id ASC LIMIT 1000")
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
        df = pd.DataFrame(result_json)
        df['day'] = pd.to_datetime(df['day'], unit='ms')
        df['time_of_the_day'] = pd.to_timedelta(df['time_of_the_day'], unit='ms')

        return df
    else:
        print('POST request failed with status code:', response.status_code)
        return None


@app.route('/get_stock_plot', methods=['POST'])
def get_stock_plot():
    try:
        # get json data, which contains stock name, time frame
        json_data = request.json
        # print(json_data)

        # fake data from database
        df = query_transaction_data()
        if df is not None:
            # generate plot
            img_base64 = generate_plot(df)


        return jsonify({'image': img_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5011)
