#dont forget to run this
#flask run
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import os



app = Flask(__name__)

CORS(app)

# Global variable to store the loaded model
loaded_model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatBot')
def chatBot():
    return render_template('chatBot.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

from py.rrwebFunctions import delete_jsons, generate_events, save_json, download_video
@app.route('/delete-jsons', methods=['POST'])
def delete_jsons_route():
    return delete_jsons()
@app.route("/api/generate-video", methods=["POST"])
def generate_events_route():
    return generate_events()
@app.route("/api/save-json", methods=["POST"])
def save_json_route():
    return save_json()
@app.route("/download-video/<session_id>", methods=["GET"])
def download_video_route(session_id):
    return download_video(session_id)

from py.chatBotFunctions import preload_model, send_message
@app.route('/api/preload-model', methods=['POST'])
def preload_model_route():
    return preload_model()
@app.route('/api/send-message', methods=['POST'])
def send_message_route():
    return send_message()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from environment or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
