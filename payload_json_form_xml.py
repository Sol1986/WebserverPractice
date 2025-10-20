from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET  # for XML parsing

app = Flask(__name__)

# -------------------------------
# 1️⃣  FORM DATA EXAMPLE
# -------------------------------
# This simulates receiving data from an HTML form (like <form method="POST">)

@app.route('/form', methods=['POST'])
def form_example():
    # Flask parses form fields for you automatically
    name = request.form.get('name', 'Unknown')
    age = request.form.get('age', 'N/A')
    return f"Received form data: name={name}, age={age}"

# -------------------------------
# 2️⃣  JSON DATA EXAMPLE
# -------------------------------
# Modern apps usually send JSON data (e.g., from JavaScript frontends or APIs)

@app.route('/json', methods=['POST'])
def json_example():
    # Convert the incoming JSON payload into a Python dictionary
    data = request.get_json(force=True)
    name = data.get('name', 'Unknown')
    age = data.get('age', 'N/A')
    return jsonify(message=f"Received JSON: {name}, age {age}")

# -------------------------------
# 3️⃣  XML DATA EXAMPLE
# -------------------------------
# XML is less common today, but still used in some older systems or integrations.

@app.route('/xml', methods=['POST'])
def xml_example():
    xml_data = request.data.decode('utf-8')  # raw bytes → string
    try:
        # Parse the XML string
        root = ET.fromstring(xml_data)
        name = root.find('name').text if root.find('name') is not None else 'Unknown'
        age = root.find('age').text if root.find('age') is not None else 'N/A'
        return f"Received XML: name={name}, age={age}"
    except Exception as e:
        return f"Invalid XML! Error: {e}", 400

# -------------------------------
# Default route for testing
# -------------------------------

@app.route('/')
def home():
    return """
    <h2>Payload Demo</h2>
    <p>Try sending POST requests to:</p>
    <ul>
        <li><code>/form</code> → with form data</li>
        <li><code>/json</code> → with JSON data</li>
        <li><code>/xml</code> → with XML data</li>
    </ul>
    """

# -------------------------------
# Run the app
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
