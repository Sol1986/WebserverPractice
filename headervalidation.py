from flask import Flask, request, jsonify, abort
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)

# 🧱 Middleware
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(f"[Middleware] Request path: {environ.get('PATH_INFO')}")
        return self.app(environ, start_response)


# 🧩 Validation schema for JSON data
class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    email = fields.Email(required=False)

user_schema = UserSchema()

# 🏠 Route: Home
@app.route('/')
def home():
    return "Welcome to the home page!"




# 🧾 Route: Capture and Validate Headers
@app.route('/api/headers', methods=['POST'])
def handle_headers():
    # Capture all headers
    all_headers = dict(request.headers)
    print("\n[Headers Received]")
    for key, value in all_headers.items():
        print(f"{key}: {value}")

    # 1️⃣ Required headers we expect
    required_headers = ["Content-Type", "X-API-Key"]

    # 2️⃣ Check for missing headers
    missing_headers = [h for h in required_headers if h not in request.headers]

    if missing_headers:
        return jsonify({
            "error": "Missing required headers",
            "missing": missing_headers
        }), 400
    

    # 3️⃣ Validate API key value
    # you can access them using: request.headers.get("Header-Name")
    api_key = request.headers.get("X-API-Key")
    if api_key != "my-secret-key":
        return jsonify({
            "error": "Invalid API key provided"
        }), 401

    # 4️⃣ Validate Content-Type
    # you can access them using: request.headers.get("Header-Name")
    content_type = request.headers.get("Content-Type")
    if content_type.lower() != "application/json":
        return jsonify({
            "error": "Unsupported Content-Type. Must be 'application/json'"
        }), 415

    # 5️⃣ Handle JSON body if headers are OK
    try:
        json_data = request.get_json()
        validated_data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    # ✅ Everything is valid
    return jsonify({
        "message": "Request accepted!",
        "headers_received": all_headers,
        "validated_data": validated_data
    }), 200


# 🧱 Apply middleware
if __name__ == '__main__':
    app.wsgi_app = SimpleMiddleware(app.wsgi_app)
    app.run(debug=True)
