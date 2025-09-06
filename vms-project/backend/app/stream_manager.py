# backend/app/streams.py
import cv2
import asyncio
import uuid
import time

streams = {}   # stream_id -> stream dict
results = {}   # result_id -> result dict

async def run_stream(stream_entry, broadcaster=None):
    stream_entry["status"] = "running"
    cap = cv2.VideoCapture(stream_entry["source"])
    if not cap.isOpened():
        print(f"❌ Could not open stream {stream_entry['source']}")
        stream_entry["status"] = "stopped"
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_idx = 0

    while stream_entry.get("running", True):
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        # Dummy motion detection
        motion_detected = frame_idx % 30 == 0
        for model_name in stream_entry["models"]:
            output = {"motion": motion_detected} if model_name == "motion_detector" else {"error": f"Model {model_name} not found"}
            result_id = str(uuid.uuid4())
            results[result_id] = {
                "id": result_id,
                "stream_id": stream_entry["id"],
                "model": model_name,
                "output": output,
                "timestamp": time.time()
            }

            # Broadcast alert if motion detected
            if motion_detected and broadcaster:
                await broadcaster.broadcast({
                    "type": "alert",
                    "alert": {
                        "stream_id": stream_entry["id"],
                        "model": model_name,
                        "message": "Motion detected!",
                        "output": output
                    }
                })

        stream_entry["fps"] = fps
        await asyncio.sleep(1.0 / fps)

    cap.release()
    stream_entry["status"] = "stopped"
