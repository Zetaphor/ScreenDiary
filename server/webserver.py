from flask import Flask, request, render_template, jsonify
import threading
from server.logger_config import get_logger
import server.api as api
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

app = Flask(__name__, template_folder='../frontend', static_folder='../captures')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summary', methods=['GET'])
def summary():
    return jsonify(api.summary())

@app.route('/search_ocr', methods=['POST'])
def post_data():
    data = request.form['query']
    return jsonify(api.search_ocr(data))

def start():
    logger.info('Startup complete, user interface running on http://localhost:' + str(SERVER_PORT))

    # Suppress Flask logging
    # sys.stdout = open(os.devnull, 'w')
    # sys.stderr = open(os.devnull, 'w')
    app.run(port=SERVER_PORT, debug=False)

def start_web_server():
    flask_thread = threading.Thread(target=start)
    flask_thread.start()
