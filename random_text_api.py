from flask import Flask, Response, jsonify, render_template_string
import threading
import time
import random
import string
import json

app = Flask(__name__)

# Client-Side HTML Template
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Random Text Stream</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        #randomText {
            font-size: 2em;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>Random Text Stream</h1>
    <div id="randomText">Connecting...</div>

    <script>
        var source = new EventSource('/random_text_stream');
        source.onmessage = function(event) {
            var data = JSON.parse(event.data);
            document.getElementById('randomText').innerHTML = data.text;
        };
        source.onerror = function(event) {
            document.getElementById('randomText').innerHTML = "Error connecting to server.";
        };
    </script>
</body>
</html>
'''

def generate_random_strings():
    while True:
        # Generate a random string of length 10
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        # Create a JSON object
        data = {'text': random_str}
        # Yield the JSON data in SSE format
        yield f"data: {json.dumps(data)}\n\n"
        # Wait for 1 second
        time.sleep(1)

@app.route('/')
def index():
    # Render the HTML template
    return render_template_string(html_template)

@app.route('/random_text_stream')
def random_text_stream():
    # Return a streaming response using SSE
    return Response(generate_random_strings(), mimetype='text/event-stream')

@app.route('/random_text', methods=['GET'])
def random_text():
    # Generate a new random string and return it as JSON
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return jsonify({'text': random_str})

if __name__ == '__main__':
    # Run the app on all available IP addresses of the host
    app.run(host='0.0.0.0', port=5000)