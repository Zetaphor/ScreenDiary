from flask import Flask, request, render_template
import threading
from server.logger_config import get_logger
from dotenv import load_dotenv
import os
import sys

load_dotenv()
logger = get_logger()

SERVER_PORT = int(os.getenv('SERVER_PORT'))
DEBUG = bool(int(os.getenv('DEBUG')))

# Hide Flask debug banner
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__, template_folder='./user_interface/content', static_folder='./user_interface/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    # Accessing GET parameters
    param1 = request.args.get('param1')  # Replace 'param1' with your actual parameter name
    param2 = request.args.get('param2')  # Example for another parameter

    # You can also provide a default value if the parameter is not found
    # param1 = request.args.get('param1', default_value)

    # Use the parameters as needed
    return f"Received GET request with param1: {param1}, param2: {param2}"

@app.route('/data', methods=['POST'])
def post_data():
    # Handle a POST request
    data = request.form['data']
    return f"Data received via POST: {data}"

def start():
    logger.info('Startup complete, user interface running on http://localhost:' + str(SERVER_PORT))

    # Suppress Flask logging
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    app.run(port=SERVER_PORT, debug=False)

def start_web_server():
    flask_thread = threading.Thread(target=start)
    flask_thread.start()
