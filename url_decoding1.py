from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the home page!"

@app.route('/hello')
def hello():
    # Flask automatically parses the query string for you
    # request.args is like a dictionary that holds all query parameters.
    # .get('name') extracts the value of name from the query string.
    # http://127.0.0.1:5000/hello?name=John%20Smith
    name = request.args.get('name', 'Guest')  # Guest is the fallback if no name is given
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run()
