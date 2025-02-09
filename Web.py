# This version of model is AI Generated, main.py is the my main idea and main project, I tried this to give it a UI.
# Still looking for a Web Developer to help me in this!
from flask import Flask, render_template_string, Response, jsonify, request
import cv2
import time
import threading

app = Flask(__name__)

# Global configuration
config = {
    "detection_enabled": True,
    "face_scale": 1.3,
    "face_neighbors": 3,
    "eye_scale": 1.1,
    "eye_neighbors": 5,
    "alarm_duration": 5,
    "last_eye_detection": time.time(),
    "alarm_active": False,
    "canny_th1": 100,
    "canny_th2": 200
}

# Load Haar Cascades
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

def generate_processed_feed():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Convert to Canny edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny_frame = cv2.Canny(blurred, config['canny_th1'], config['canny_th2'])
        output_frame = cv2.cvtColor(canny_frame, cv2.COLOR_GRAY2BGR)

        if config['detection_enabled']:
            # Face and eye detection
            faces = face_cascade.detectMultiScale(
                gray, 
                scaleFactor=config['face_scale'],
                minNeighbors=config['face_neighbors']
            )
            
            eyes_detected = False
            for (x, y, w, h) in faces:
                cv2.rectangle(output_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h//2, x:x+w]
                eyes = eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=config['eye_scale'],
                    minNeighbors=config['eye_neighbors']
                )
                if len(eyes) > 0:
                    eyes_detected = True
                    config['last_eye_detection'] = time.time()
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(output_frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

            # Update alarm status
            config['alarm_active'] = time.time() - config['last_eye_detection'] > config['alarm_duration']
            if config['alarm_active']:
                cv2.putText(output_frame, "WAKE UP!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        _, buffer = cv2.imencode('.jpg', output_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Eye Detection Monitor</title>
        <style>
            body { margin: 0; padding: 20px; background: #1a1a1a; color: white; }
            .container { display: grid; grid-template-columns: 300px 1fr; gap: 20px; }
            .video-container { border: 2px solid #2196F3; border-radius: 8px; }
            .controls { background: #2a2a2a; padding: 20px; border-radius: 8px; }
            .slider-container { margin: 15px 0; }
            button { background: #2196F3; color: white; border: none; padding: 10px 20px; margin: 5px; }
            #alarmStatus { color: red; font-weight: bold; display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="controls">
                <h2>Controls</h2>
                <button id="toggleDetection">{{ 'ON' if config.detection_enabled else 'OFF' }}</button>
                <div class="slider-container">
                    <label>Canny Threshold 1: <span id="th1Value">100</span></label>
                    <input type="range" id="cannyTh1" min="1" max="300" value="100">
                </div>
                <div class="slider-container">
                    <label>Canny Threshold 2: <span id="th2Value">200</span></label>
                    <input type="range" id="cannyTh2" min="1" max="300" value="200">
                </div>
                <div id="alarmStatus">ALARM ACTIVE!</div>
            </div>
            <div class="video-container">
                <img id="processedFeed" src="/processed_feed">
            </div>
        </div>

        <audio id="alarmSound" src="/static/beep.mp3"></audio>

        <script>
            // Toggle detection
            const toggleBtn = document.getElementById('toggleDetection');
            toggleBtn.addEventListener('click', () => {
                fetch('/toggle_detection')
                    .then(() => toggleBtn.textContent = 
                        toggleBtn.textContent === 'ON' ? 'OFF' : 'ON');
            });

            // Canny threshold controls
            document.getElementById('cannyTh1').addEventListener('input', e => {
                document.getElementById('th1Value').textContent = e.target.value;
                updateConfig({ canny_th1: parseInt(e.target.value) });
            });

            document.getElementById('cannyTh2').addEventListener('input', e => {
                document.getElementById('th2Value').textContent = e.target.value;
                updateConfig({ canny_th2: parseInt(e.target.value) });
            });

            // Audio handling with user interaction
            let audioAllowed = false;
            const alarmSound = document.getElementById('alarmSound');
            
            document.body.addEventListener('click', () => {
                if (!audioAllowed) {
                    audioAllowed = true;
                    alarmSound.play().then(() => alarmSound.pause());
                }
            });

            // Alarm check loop
            setInterval(async () => {
                if (!audioAllowed) return;
                
                const response = await fetch('/alarm_status');
                const data = await response.json();
                
                if (data.alarm_active) {
                    alarmSound.play();
                    document.getElementById('alarmStatus').style.display = 'block';
                } else {
                    alarmSound.pause();
                    alarmSound.currentTime = 0;
                    document.getElementById('alarmStatus').style.display = 'none';
                }
            }, 1000);

            function updateConfig(data) {
                fetch('/update_config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/processed_feed')
def processed_feed():
    return Response(generate_processed_feed(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_detection')
def toggle_detection():
    config['detection_enabled'] = not config['detection_enabled']
    return jsonify(success=True)

@app.route('/update_config', methods=['POST'])
def update_config():
    data = request.json
    for key in data:
        if key in config:
            config[key] = data[key]
    return jsonify(success=True)

@app.route('/alarm_status')
def alarm_status():
    return jsonify(alarm_active=config['alarm_active'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
