from flask import Flask, request

app = Flask(__name__)

# 🧱 Middleware: Runs before each request
@app.before_request
def before_request_func():
    print(f"[Middleware] Incoming request: {request.method} {request.path}")

# 🧱 Middleware: Runs after each request
@app.after_request
def after_request_func(response):
    print(f"[Middleware] Response status: {response.status}")
    # You can also modify the response here, e.g. add headers:
    # Right-click → Inspect → Network tab Click on the /hello request. Under Response Headers, you’ll see it
    # curl -i http://127.0.0.1:5000/hello?name=John
    response.headers["X-Powered-By"] = "Flask Middleware"
    return response

@app.route('/')
def home():
    return "Welcome to the home page!"

# http://127.0.0.1:5000/hello?name=john%20smith
@app.route('/hello')
def hello():
    # In Flask, you can read those query parameters using request.args
    name = request.args.get('name', 'Guest')
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True)
