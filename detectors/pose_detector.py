from ultralytics import YOLO

class PoseDetector:
    def __init__(self):
        self.model = YOLO('yolov8n-pose.pt')

    def detect_pose(self, frame):
        results = self.model(frame, imgsz=320, conf=0.5, verbose=False)

        return results
    
    def draw_pose(self, frame, results):
        annotated_frame = results[0].plot()

        return annotated_frame
    
    def extract_keypoints(self, results):
        if results[0].keypoints is None:
            return None
        
        keypoints = results[0].keypoints.xy.cpu().numpy()
        return keypoints 
    
