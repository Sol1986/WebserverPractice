from flask import Flask, request, abort

# Create the app
app = Flask(__name__)

# --------------------------
# 1️⃣ STATIC ROUTES
# --------------------------

@app.route('/')
def home():
    return "Welcome to the homepage! 🏠"

@app.route('/about')
def about():
    return "This is the About page."

@app.route('/cats')
def cats():
    return "This action returns all cats. 🐱"

# --------------------------
# 2️⃣ NESTED ROUTES
# --------------------------

@app.route('/animals/cats')
def animals_cats():
    return "Nested route: animals/cats → Meow!"

@app.route('/animals/dogs')
def animals_dogs():
    return "Nested route: animals/dogs → Woof!"

# --------------------------
# 3️⃣ PATH PARAMETERS
# --------------------------

# Example: /user/Alice
@app.route('/user/<username>')
def show_user(username):
    return f"Hello, {username}! 🧑"

# Example: /post/123
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Showing post #{post_id}"

# --------------------------
# 4️⃣ MULTIPLE ROUTES (Pattern-Based)
# --------------------------

@app.route('/cat')
@app.route('/cats-list')
def cat_alias():
    return "This shows all cats (same function, two routes)."

# --------------------------
# 5️⃣ QUERY PARAMETERS (from URL)
# --------------------------

# Example: /greet?name=John
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    return f"Hello, {name}!"

# --------------------------
# 6️⃣ MIDDLEWARE (runs before each request)
# --------------------------

@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.path}")

# --------------------------
# 7️⃣ ERROR HANDLING
# --------------------------

@app.errorhandler(404)
def not_found(e):
    return "Oops! Page not found (404).", 404

@app.errorhandler(403)
def forbidden(e):
    return "Access forbidden (403).", 403

# --------------------------
# 8️⃣ GUARD / FILTER (Protect route)
# --------------------------

@app.route('/admin')
def admin():
    logged_in = request.args.get('logged_in')
    if logged_in != 'true':
        abort(403)  # Forbidden
    return "Welcome to the admin panel. 🔒"

# --------------------------
# RUN THE SERVER
# --------------------------

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True) # goes on a different port
