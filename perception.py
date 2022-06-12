import cv2
import time
import threading

class VideoStream:
    def __init__(self, stream_address, fps=5.0):
        self.address = stream_address
        self.connect()
        self.connected = False
        self.frame_read = False

        self.wait_time = 1 / fps

    def start(self):
        while self.connected:
            ret, frame = self.cap.read()
            self.frame_read = frame
            time.sleep(self.wait_time)

    def connect(self):
        self.cap = cv2.VideoCapture(self.address)
        while not self.cap.isOpened():
            print("Connecting to the camera...")
            time.sleep(5)
        self.connected = True
        print("Connected")

class FramePreprocessor:
    def __init__(self, video_stream, n_frames, fps, size=(128, 128)):
        self.video_stream = video_stream
        self.n_frames = n_frames
        self.wait_time = 1 / fps
        self.size = size
        self.video_stream.start()

    def preprocess(self):
        # get the most recent n_frames frames from the stream
        frame_data = []
        for i in range(self.n_frames):
            data = cv2.resize(self.video_stream.frame_read, self.size)
            frame_data.append(data)
            time.sleep(self.wait_time)
        # format correctly and return
        return frame_data

class SensorPreprocessor:
    def __init__(self, roomba_adapter, n_steps, fps):
        self.roomba = roomba_adapter
        self.n_steps = n_steps
        self.wait_time = 1 / fps
        
    def preprocess(self):
        # get the most recent n_steps of sensory data from the roomba
        sensor_data = []
        for i in range(self.n_steps):
            data = self.roomba.request_data()
            sensor_data.append(int.from_bytes(data, 'little'))
            time.sleep(self.wait_time)
        # format it correctly and return
        return sensor_data
