from flask import Flask, request, jsonify, send_from_directory
import threading
import time
import os
import json
from datetime import datetime
from finalcode import download_video, play_videos
from syslog import log_video_played

app = Flask(__name__)
playback_thread = None
should_stop = False

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def js():
    return send_from_directory('.', 'script.js')

@app.route('/download', methods=['POST'])
def handle_download():
    try:
        download_video()
        return "✅ Videos downloaded successfully."
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/start-playback', methods=['POST'])
def start_playback():
    global playback_thread, should_stop

    data = request.json
    end_time_str = data.get('end_time')
    screenshots = data.get('screenshots', False)

    if not end_time_str:
        return "❌ End time is required.", 400

    end_time = datetime.fromisoformat(end_time_str)

    # Launch playback in a new thread
    should_stop = False
    playback_thread = threading.Thread(target=playback_worker, args=(end_time, screenshots))
    playback_thread.start()
    return "▶️ Playback started."

def playback_worker(end_time, screenshots):
    global should_stop
    counter = 0

    try:
        while datetime.now() < end_time and not should_stop:
            play_videos(counter)
            counter += 1
            if should_stop:
                break
    except Exception as e:
        print("Playback error:", e)

@app.route('/stop', methods=['POST'])
def stop_playback():
    global should_stop
    should_stop = True
    return "⛔ Playback stopped."

@app.route('/logs')
def get_logs():
    try:
        if os.path.exists("video_log.json"):
            with open("video_log.json", "r") as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
