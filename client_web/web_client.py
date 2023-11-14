from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# backend request url
API_URL = "https://jsonplaceholder.typicode.com/posts"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')

    response = requests.get(API_URL, params={'q': keyword})

    if response.status_code == 200:
        data = response.json()
        # Add fake json data
        fake_data = [
                {"service_id": 101, "title": "stock overtime performance check", "ip": "127.0.0.1", "port":"5009"},
                {"service_id": 102, "title": "stock notifications", "ip": "127.0.0.1", "port":"5010"},
        ]

        # Uncomment the line below to use fake data for testing
        return render_template('search_results.html', results=fake_data)
        return render_template('search_results.html', results=data)
    else:
        return "Error fetching data from the registry server!"

if __name__ == '__main__':
    app.run(debug=True, port=5005)
