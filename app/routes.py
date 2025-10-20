
#Now we define all routes (endpoints) in one place and import the schema.

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.schemas import UserSchema
from flasgger import swag_from

main = Blueprint('main', __name__)
user_schema = UserSchema()

@main.route('/')
def home():
    """Home endpoint
    ---
    responses:
      200:
        description: Returns a welcome message.
    """
    return "Welcome to the home page!"


@main.route('/api/headers', methods=['POST'])
@swag_from({
    'tags': ['Header and Data Validation'],
    'description': 'Validates headers and JSON payload.',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
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
        200: {'description': 'Request accepted'},
        400: {'description': 'Missing headers or invalid data'},
        401: {'description': 'Invalid API key'}
    }
})
def handle_headers():
    # Header validation
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "Missing X-API-Key header"}), 400
    if api_key != "my-secret-key":
        return jsonify({"error": "Invalid API key"}), 401

    # JSON validation
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
