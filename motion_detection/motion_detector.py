import cv2
import numpy as np
from datetime import datetime
from threading import Thread
import time

class MotionDetector:
    def __init__(self, min_motion_area=250, threshold=25):
        self.min_motion_area = min_motion_area
        self.threshold = threshold
        self.previous_frame = None
        self.motion_detected = False
        self.last_motion_time = None
        self.motion_history = []
        self.notification_active = False
        self.notification_message = ""
        self.running = True
        
        # Start notification thread
        self.notification_thread = Thread(target=self._generate_notifications, daemon=True)
        self.notification_thread.start()

    def detect_motion(self, frame):
        # Convert to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Initialize previous frame if needed
        if self.previous_frame is None:
            self.previous_frame = gray
            return False, frame
        
        # Compute absolute difference between current and previous frame
        frame_delta = cv2.absdiff(self.previous_frame, gray)
        thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate the threshold image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        self.motion_detected = False
        
        # Check each contour
        for contour in contours:
            if cv2.contourArea(contour) < self.min_motion_area:
                continue
                
            self.motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Update previous frame
        self.previous_frame = gray
        
        # Update motion history
        if self.motion_detected:
            self.last_motion_time = datetime.now()
            self.motion_history.append(self.last_motion_time)
            # Keep only the last 100 detections
            if len(self.motion_history) > 100:
                self.motion_history.pop(0)
        
        return self.motion_detected, frame

    def _generate_notifications(self):
        while self.running:
            if self.motion_detected and self.last_motion_time:
                time_since = datetime.now() - self.last_motion_time
                if time_since.total_seconds() < 5:  # Only notify if motion was recent
                    self.notification_active = True
                else:
                    self.notification_active = False
            else:
                self.notification_active = False
            
            time.sleep(0.1)  # Check every 100ms

    def get_status(self):
        return {
            'motion_detected': self.motion_detected,
            'last_motion_time': self.last_motion_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_motion_time else None,
            'notification_active': self.notification_active,
            'notification_message': self.notification_message
        }

    def stop(self):
        self.running = False
        self.notification_thread.join()