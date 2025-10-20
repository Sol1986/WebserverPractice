from flask import Flask, request

app = Flask(__name__)

class SimpleMiddleware:
    # A simple WSGI middleware that logs request paths
    # It wraps around the Flask application
    # and prints the request path for each incoming request
    def __init__(self, app):
        self.app = app

    # WSGI Web Server Gateway Interface.It’s the standard interface between a Python web app (like Flask) and a web server (like Werkzeug, Gunicorn, or uWSGI).
    # That means every WSGI-compatible app — including Flask — is just a callable Python object (usually a function or a class with a __call__ method) that takes exactly two arguments:
    # start_response: a callable provided by the server to start the HTTP response
    # environ: a dictionary containing request info
    # The __call__ method is a special Python method. It lets an object act like a function.
    # When you call an instance of a class that has a __call__ method, Python invokes that method.
    # Here, it allows our SimpleMiddleware class to be used as a WSGI application.
    def __call__(self, environ, start_response):
        # environ contains all request info
        print(f"[Middleware] Request path: {environ.get('PATH_INFO')}")
        # Call the original Flask app
        return self.app(environ, start_response)


@app.route('/')
def home():
    return "Welcome to the home page!"

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    return f"Hello, {name}!"

# Run the app
# The middleware is applied by wrapping the Flask app's WSGI application. 
if __name__ == '__main__':
    app.wsgi_app = SimpleMiddleware(app.wsgi_app)
    app.run(debug=True)

# curl -i http://127.0.0.1:5000/hello?name=John