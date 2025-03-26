import cv2
from flask import Flask, render_template, Response
import atexit

app = Flask(__name__)
for i in range(10):  # Try up to 10 camera indices
    video = cv2.VideoCapture(i)
    if video.isOpened():
        print(f"Camera found on index {i}")
        break
else:
    raise RuntimeError("Could not open any camera")

if not video.isOpened():
    raise RuntimeError("Could not open camera on /dev/video1")

def release_camera():
    video.release()

atexit.register(release_camera)

def video_stream():
    while True:
        success, frame = video.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)