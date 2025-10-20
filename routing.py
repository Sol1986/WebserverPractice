from flask import Flask

app = Flask(__name__)

# Route 1 - Home Page
@app.route('/')
def home():
    return "Welcome to the Home Page!"

# Route 2 - About Page
@app.route('/about')
def about():
    return "This is the About Page."
# Route 3 - Contact Page

@app.route('/contact')
def contact():
    return "This is the Contact Page."

# Route 3 - Dynamic User Page
# You can capture parts of the URL using angle brackets < >:
@app.route('/user/<username>')
def show_user_profile(username):
    return f"User: {username}"

# Route 4 - API-style route with optional methods
@app.route('/add', methods=['GET'])
def add():
    a = 5
    b = 10
    return f"The sum of {a} and {b} is {a + b}"

# Route 5 - Dynamic Post Page
# Visiting /post/5 passes post_id = 5 as an integer.
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Showing post #{post_id}"


if __name__ == '__main__':
    app.run()