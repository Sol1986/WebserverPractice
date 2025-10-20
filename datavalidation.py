#pip install marshmallow
#pip install flask-expects-json

from flask import Flask, request, jsonify, abort
from flask_expects_json import expects_json    
from marshmallow import Schema, fields, ValidationError
import json

app = Flask(__name__)



# 🧱 Middleware (still here)
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(f"[Middleware] Request path: {environ.get('PATH_INFO')}")
        return self.app(environ, start_response)




# 🧩 Marshmallow Schema for validation
class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    email = fields.Email(required=False)

user_schema = UserSchema()




# 🧱 Route 1: Home
@app.route('/')
def home():
    return "Welcome to the home page!"


# 🧱 Route 2: Validate JSON data
@app.route('/api/validate', methods=['POST'])
def validate_user():
    # 1️⃣ Check headers first
    api_key = request.headers.get('X-API-Key')
    if api_key != "my-secret-key":
        return jsonify({"error": "Unauthorized: missing or invalid API key"}), 401

    # 2️⃣ Parse JSON from request body
    try:
        json_data = request.get_json(force=True)  # Flask auto-deserializes JSON → dict
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    # 3️⃣ Validate data against schema
    try:
        validated_data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400

    # 4️⃣ If valid, return a success message
    return jsonify({
        "message": "User data validated successfully!",
        "validated_data": validated_data
    }), 200


# Define a schema (rules for valid JSON)
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "email"]
}


# 🧱 Route 3: Validate JSON data
@app.route('/register', methods=['POST'])
@expects_json(schema)
def register():
    from flask import request
    data = request.get_json()
    return jsonify(message="Valid data received!", data=data)


# 🧱 Apply middleware
if __name__ == '__main__':
    app.wsgi_app = SimpleMiddleware(app.wsgi_app)
    app.run(debug=True)
