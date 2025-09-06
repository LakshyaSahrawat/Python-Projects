# backend/app/model_registry.py
import cv2
import numpy as np

class ModelRegistry:
    def __init__(self):
        self.models = {
            "motion_detector": self.motion_detector
        }

    def predict(self, model_name, frame, stream_id=None):
        model = self.models.get(model_name)
        if not model:
            return {"error": f"Model {model_name} not found"}

        return model(frame)

    def motion_detector(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if not hasattr(self, "first_frame"):
            self.first_frame = gray
            return {"alert": False, "message": "No motion detected"}

        frame_delta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_percent = np.sum(thresh) / (thresh.size * 255) * 100

        alert = motion_percent > 2  # motion threshold
        return {"alert": alert, "message": "Motion detected" if alert else "No motion"}
