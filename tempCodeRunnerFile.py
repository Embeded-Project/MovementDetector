from flask import Flask, render_template, Response, jsonify, request
import cv2
import atexit
from motion_detection.motion_detector import MotionDetector

app = Flask(__name__)

# Initialize camera
for i in range(10):
    video = cv2.VideoCapture(i)
    if video.isOpened():
        print(f"Camera found on index {i}")
        break
else:
    raise RuntimeError("Could not open any camera")

# Initialize motion detector
motion_detector = MotionDetector(min_motion_area=500, threshold=25)
system_armed = False  # Global state for arm/disarm

def release_resources():
    video.release()
    motion_detector.stop()

atexit.register(release_resources)

def video_stream():
    while True:
        success, frame = video.read()
        if not success:
            break
        
        # Only detect motion if system is armed
        if system_armed:
            motion_detected, processed_frame = motion_detector.detect_motion(frame)
            
            if motion_detector.notification_active:
                cv2.putText(processed_frame, "ALERT: Motion Detected", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
        else:
            processed_frame = frame
            cv2.putText(processed_frame, "System Disarmed", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/motion_status')
def motion_status():
    status = motion_detector.get_status()
    status['system_armed'] = system_armed
    return jsonify(status)

@app.route('/toggle_arm', methods=['POST'])
def toggle_arm():
    global system_armed
    system_armed = not system_armed
    return jsonify({'armed': system_armed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)