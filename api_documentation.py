# pip install flasgger
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError
from flasgger import Swagger, swag_from

app = Flask(__name__)

# 🧠 Initialize Swagger
#swagger = Swagger(app)

swagger = Swagger(app, template={
    "info": {
        "title": "Flask Learning API",
        "description": "A demo API with middleware, headers, and validation",
        "version": "1.0.0"
    }
})


# 🧩 Middleware (still logging all requests)
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(f"[Middleware] Request path: {environ.get('PATH_INFO')}")
        return self.app(environ, start_response)


# 🧱 Marshmallow Schema for validation
class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    email = fields.Email(required=False)

user_schema = UserSchema()


# 🏠 Basic route
@app.route('/')
def home():
    """Home endpoint
    ---
    responses:
      200:
        description: Returns a welcome message.
    """
    return "Welcome to the home page!"


# 🧾 Route with headers and JSON validation
@app.route('/api/headers', methods=['POST'])
@swag_from({
    'tags': ['Header and Data Validation'],
    'description': 'Validates headers and body JSON payload.',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
        },
        {
            'name': 'Content-Type',
            'in': 'header',
            'type': 'string',
            'required': True,
            'default': 'application/json'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'age': {'type': 'integer'},
                    'email': {'type': 'string'}
                },
                'required': ['name', 'age']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Request accepted and validated.',
            'examples': {
                'application/json': {
                    'message': 'Request accepted!',
                    'validated_data': {
                        'name': 'Alice',
                        'age': 25,
                        'email': 'alice@example.com'
                    }
                }
            }
        },
        400: {'description': 'Missing headers or invalid data'},
        401: {'description': 'Invalid API key'}
    }
})
def handle_headers():
    """Handle Headers and JSON Data"""
    # 1️⃣ Check headers
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "Missing X-API-Key header"}), 400
    if api_key != "my-secret-key":
        return jsonify({"error": "Invalid API key"}), 401

    # 2️⃣ Validate content type
    if request.headers.get("Content-Type") != "application/json":
        return jsonify({"error": "Content-Type must be application/json"}), 415

    # 3️⃣ Validate JSON body
    try:
        json_data = request.get_json()
        validated_data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    return jsonify({
        "message": "Request accepted!",
        "validated_data": validated_data
    }), 200


# 🧱 Apply middleware
if __name__ == '__main__':
    app.wsgi_app = SimpleMiddleware(app.wsgi_app)
    app.run(debug=True)
