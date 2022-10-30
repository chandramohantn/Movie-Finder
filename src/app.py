import json
from flask import Flask, request, render_template
from db_operations.crud import get_movie_from_tbl

with open("app_config.json", "r") as fp:
    db_config = json.load(fp)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/get_movie', methods=["POST"])
def get_movie():
    content_type = request.headers.get('Content-Type')
    assert content_type == 'application/json', 'Content-Type not supported!'
    query = request.json
    print(query)
    print(query['cast'])
    cast = query['cast'].split(',')
    response = get_movie_from_tbl(cast)
    return response


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
