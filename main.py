from flask import Flask, render_template, request
import json

app = Flask(__name__)
config = json.loads(open('config.json').read())
api_key = config['API_KEY']


@app.route('/', methods=['GET'])
def index():
    print(api_key)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
