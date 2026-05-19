import cv2

from core.video_stream import VideoStream
from core.fps_monitor import FPSMonitor
from detectors.pose_detector import PoseDetector

video_stream = VideoStream()
fps_monitor = FPSMonitor()
pose_detector = PoseDetector()

while True:
    frame = video_stream.read_frame()
    fps = fps_monitor.update()

    if frame is None:
        break

    pose_results = pose_detector.detect_pose(frame)
    frame = pose_detector.draw_pose(frame, pose_results)
    keypoints = pose_detector.extract_keypoints(pose_results)

    if keypoints is not None:
        print(keypoints.shape)

    cv2.putText(frame, f'FPS: {fps}', (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow('Human Attention Monitor', frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

video_stream.release()
cv2.destroyAllWindows()