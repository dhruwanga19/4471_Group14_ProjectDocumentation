from flask import Flask, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from flask_cors import CORS
import numpy as np
import io
import base64

# Fake data
x = np.linspace(0, 10, 100)
y = np.sin(x)

app = Flask(__name__)
CORS(app)

def generate_plot():
    # fetch data from database server
    # currently using fake data

    # generate plot image
    plt.plot(x, y, label='Sin(x)')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Simple Plot with Fake Data')

    # save the image to ram and sent via http request
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # conver the imge_buffer to base64 encoding
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

    plt.clf()

    return img_base64


@app.route('/get_stock_plot', methods=['POST'])
def get_stock_plot():
    try:
        # get json data, which contains stock name, time frame
        # json_data = request.json
        # print(json_data)

        # fake data from database

        # generate plot
        img_base64 = generate_plot()

        return jsonify({'image': img_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5011)
