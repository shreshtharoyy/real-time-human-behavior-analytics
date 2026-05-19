import cv2

from core.video_stream import VideoStream
from core.fps_monitor import FPSMonitor
from detectors.pose_detector import PoseDetector

video_stream = VideoStream()
fps_monitor = FPSMonitor()
pose_detector = PoseDetector()

distraction_counter = 0

while True:
    frame = video_stream.read_frame()
    fps = fps_monitor.update()

    if frame is None:
        break

    pose_results = pose_detector.detect_pose(frame)
    frame = pose_detector.draw_pose(frame, pose_results)
    keypoints = pose_detector.extract_keypoints(pose_results)

    attention_state = "NO PERSON DETECTED"
    posture_state = "NO POSTURE DATA"

    if keypoints is not None and len(keypoints)>0:
        person = keypoints[0]
        nose = person[0]
        left_eye = person[1]
        right_eye = person[2]
        left_shoulder = person[5]
        right_shoulder = person[6]

        shoulder_center_x = (left_shoulder[0] + right_shoulder[0]) / 2
        nose_x = nose[0]

        if nose_x < shoulder_center_x - 40:
            attention_state = "HEAD TURNED RIGHT"

        elif nose_x > shoulder_center_x + 40:
            attention_state = "HEAD TURNED LEFT"

        else:
            attention_state = "ATTENTIVE"


        if attention_state != "ATTENTIVE":
            distraction_counter += 1

        else:
            distraction_counter = 0

        if distraction_counter > fps * 5:
            cv2.putText(frame, "PROLONGED DISTRACTION", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


        left_shoulder_y = left_shoulder[1]
        right_shoulder_y = right_shoulder[1]

        shoulder_avg_y = (left_shoulder_y + right_shoulder_y) / 2

        if shoulder_avg_y > 440:
            posture_state = "SLOUCHING"

        else:
            posture_state = "GOOD POSTURE"  

        cv2.putText(frame, attention_state, (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, posture_state, (20,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, f'FPS: {fps}', (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow('Human Behavior Analytics Window', frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

video_stream.release()
cv2.destroyAllWindows()