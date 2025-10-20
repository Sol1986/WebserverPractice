from flask import Flask, request, abort, jsonify

app = Flask(__name__)

# 🧩 Simple Middleware
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(f"[Middleware] Request path: {environ.get('PATH_INFO')}")
        return self.app(environ, start_response)

# 🏠 Home route
@app.route('/')
def home():
    return "Welcome to the home page!"

# 👋 Simple greeting route
@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    return f"Hello, {name}!"

# 🔐 Guarded route
@app.route('/admin')
def admin():
    if not request.args.get('logged_in'):
        abort(403)  # Forbidden
    return "Welcome to the admin dashboard!"

# 💾 NEW: Route that receives JSON data
@app.route('/api/data', methods=['POST'])
def receive_data():
    # Flask automatically parses JSON if Content-Type is application/json
    # request.get_json() returns a Python dictionary from the JSON body.
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    # Extract specific fields safely
    name = data.get("name")
    age = data.get("age")

    # Simple validation
    if not name or not age:
        return jsonify({"error": "Missing 'name' or 'age' field"}), 400

    # Example: process the data
    print(f"Received JSON data: Name={name}, Age={age}")

    # Return a response as JSON
    return jsonify({
        "message": f"Hello {name}, you are {age} years old!",
        "status": "success"
    }), 200

# 🧱 Apply middleware
if __name__ == '__main__':
    app.wsgi_app = SimpleMiddleware(app.wsgi_app)
    app.run(debug=True)
