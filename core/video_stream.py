import cv2

class VideoStream:

    def __init__(self, source=0, width=640, height=480):
        self.cap = cv2.VideoCapture(source)
        self.width = width
        self.height = height

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            return None
        
        return frame
    
    def release(self):
        self.cap.release()

    