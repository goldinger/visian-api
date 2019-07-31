from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello'


@app.route('/tasks')
def get_tasks():
    return {'tasks': ['1', '2']}


if __name__ == '__main__':
    app.run()
