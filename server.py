#import Flask framework
from flask import Flask

# initialize Flask application
# This line creates an instance of the Flask application.
# The __name__ variable is a special Python variable that holds the name of the current module.
app = Flask(__name__)

#define a route for the root URL
# This decorator tells Flask to execute the hello function when the root URL ("/") is accessed.
# The function returns a simple string "hello, world!" which will be displayed in the web browser.
# When you run this Flask application and navigate to the root URL, you will see "hello, world!" displayed.
# The route() decorator is used to bind a function to a URL.
# '/' means the root URL (e.g., http://localhost:5000/).
@app.route('/')
def hello():
	return "hello, world!"

# run the application
# This block checks if the script is being run directly (not imported as a module).
# If it is, it starts the Flask development server by calling app.run().
# The server will listen for incoming requests and handle them using the defined routes.
if __name__ == '__main__':
	app.run()
