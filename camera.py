import cv2
from flask import Flask, render_template, Response
from motion_detection.motion_detector import MotionDetector
import atexit
motion_detector = MotionDetector(min_motion_area=500, threshold=25)
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
         # Detect motion
        motion_detected, processed_frame = motion_detector.detect_motion(frame)
        
        # Add notification text if active
        if motion_detector.notification_active:
            cv2.putText(processed_frame, motion_detector.notification_message, 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
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