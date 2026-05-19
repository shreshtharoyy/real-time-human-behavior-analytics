import time

class FPSMonitor:
    def __init__(self):
        self.prev_time = 0
        self.curr_time = 0

    def update(self):
        self.curr_time = time.time()
        fps = 1 / (self.curr_time - self.prev_time)
        self.prev_time = self.curr_time

        return int(fps)

