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
        return render_template('search_results.html', results=data)
    else:
        return "Error fetching data from the registry server!"

if __name__ == '__main__':
    app.run(debug=True, port=5005)
