from flask import Flask, request, abort

app = Flask(__name__)

# Simple WSGI Middleware
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(f"[Middleware] Request path: {environ.get('PATH_INFO')}")
        return self.app(environ, start_response)

# Attach the middleware
# Every time a request hits your Flask app, it first passes through SimpleMiddleware.__call__() → which prints the path (e.g., /hello, /) → then forwards the request to the real Flask app.
# So in your terminal, you’ll see something like: [Middleware] Request path: /hello
app.wsgi_app = SimpleMiddleware(app.wsgi_app)

@app.route('/')
def home():
    return "Welcome to the home page!"

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    return f"Hello, {name}!"

# 🧱 Guard-protected route
# http://127.0.0.1:5000/admin?logged_in=true
# Browser ↓ SimpleMiddleware (logs path) ↓ Flask Routing ↓ Guard (checks ?logged_in) ↓ ✅ allowed → route returns response ❌ blocked → abort(403)
@app.route('/admin')
def admin():
    # Guard / filter logic
    if not request.args.get('logged_in'):
        abort(403)  # Forbidden if user not logged in
    return "Welcome to the admin dashboard!"

if __name__ == '__main__':
    app.run(debug=True)