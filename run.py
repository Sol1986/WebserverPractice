# This is your new entry point (replaces app.py).
# It imports the create_app function from app/init.py
# and runs the Flask application.
# This keeps your application modular and organized.
# You can run this file to start your Flask server. python run.py
# Swagger UI → http://127.0.0.1:5000/apidocs/
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
