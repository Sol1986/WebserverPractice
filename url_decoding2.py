from flask import Flask, request
from urllib.parse import unquote

app = Flask(__name__)

# ---- ROUTING EXAMPLES ----

# 1️⃣ Basic route
@app.route('/')
def home():
    return "Welcome to the homepage!"

# 2️⃣ Another route
@app.route('/hello')
def hello():
    return "Hello there! 👋"

# 3️⃣ Route with query parameters
# Example: http://localhost:5000/greet?name=John%20Smith
@app.route('/greet')
def greet():
    # Get the "name" value from the URL query string
    # request.args gives you ?name=John%20Smith as a dictionary
    name = request.args.get('name', 'Guest')

    # Flask automatically decodes most things, but let's show it manually
    decoded_name = unquote(name)

    return f"Hello, {decoded_name}!"

# 4️⃣ Example for unknown routes (404)
# http://127.0.0.1:5000/blog
@app.errorhandler(404)
def not_found(e):
    return "404 - That page does not exist.", 404


# ---- RUN THE APP ----
if __name__ == '__main__':
    app.run()
