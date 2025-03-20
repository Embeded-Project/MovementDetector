import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

def get_camera():
    # Try different camera configurations
    try:
        return cv2.VideoCapture("libcamerasrc ! video/x-raw ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
    except:
        pass
    
    try:
        return cv2.VideoCapture(0)
    except:
        pass
    
    for i in range(1, 26):
        try:
            camera = cv2.VideoCapture(i)
            if camera.isOpened():
                return camera
        except:
            pass
    raise RuntimeError("Could not access any camera")

def generate_frames():
    camera = get_camera()
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Create basic HTML template

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)