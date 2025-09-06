# app/motion_detector.py
import cv2
import numpy as np

class MotionDetector:
    def __init__(self):
        self.prev_frame = None

    def predict(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.prev_frame is None:
            self.prev_frame = gray
            return {"motion": False}

        diff = cv2.absdiff(self.prev_frame, gray)
        self.prev_frame = gray
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        motion_level = np.sum(thresh) / 255
        if motion_level > 5000:  # tune threshold as needed
            return {
                "motion": True,
                "alert": True,
                "message": "Motion detected in stream"
            }

        return {"motion": False}
