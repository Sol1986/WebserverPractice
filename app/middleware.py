#Keep your middleware separate here.

class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(f"[Middleware] Request path: {environ.get('PATH_INFO')}")
        return self.app(environ, start_response)
