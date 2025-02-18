from flask import Flask, render_template, Response, request, jsonify
from main import drowsiness_detector
import cv2
import threading
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_system', methods=['POST'])
def start_system():
    data = request.get_json()
    hazard_mode = data.get('dangerMode', False)
    sound_on = data.get('soundOn', True)

    # Stop existing detection if running
    drowsiness_detector.stop_detection()
    # Start new thread
    thread = threading.Thread(target=drowsiness_detector.start_detection, 
                            kwargs={'hazard_on': hazard_mode, 'sound_on': sound_on})
    thread.start()

    return jsonify({'status': 'started', 'dangerMode': hazard_mode, 'soundOn': sound_on})

@app.route('/stop_system', methods=['POST'])
def stop_system():
    drowsiness_detector.stop_detection()
    return jsonify({'status': 'stopped'})

def gen_frames():
    while True:
        if drowsiness_detector.detection_active:
            with drowsiness_detector.frame_lock:
                if drowsiness_detector.latest_frame is not None:
                    frame = drowsiness_detector.latest_frame.copy()
                else:
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "System Inactive", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)