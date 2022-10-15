import torch
import numpy as np
import cv2
from pathlib import Path
import math
from threading import Thread
import time

class StreamLoader:
    # YOLOv5 streamloader, i.e. `python detect.py --source 'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP streams`
    def __init__(self, source, img_size=(640, 640), stride=32, auto=True, transforms=None):
        torch.backends.cudnn.benchmark = True  # faster for fixed-size inference
        self.mode = 'stream'
        self.img_size = img_size
        self.stride = stride
        self.source = source 
        self.img, self.fps, self.frame, self.thread = None, 0, 0, None
        self.count = 0
        # Start thread to read frames from video stream
        cap = cv2.VideoCapture(self.source)
        assert cap.isOpened(), f'Failed to open {self.source}'
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)  # warning: may return 0 or nan
        self.frames= max(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), 0) or float('inf')  # infinite stream fallback
        self.fps = max((fps if math.isfinite(fps) else 0) % 100, 0) or 30  # 30 FPS fallback
        _, img = cap.read()  # guarantee first frame
        #self.img = np.expand_dims(img, axis=0)
        self.img = img
        self.cap = cap
        #self.update(cap, self.source)
        self.thread = Thread(target=self.update, args=([self.cap, self.source]), daemon=True)
        #self.thread.start()
        # check for common shapes
        s = np.stack([letterbox(self.img, img_size, stride=stride, auto=auto)[0].shape])
        self.rect = np.unique(s, axis=0).shape[0] == 1  # rect inference if all shapes equal
        self.auto = auto and self.rect
        self.transforms = transforms  # optional

    def update(self, cap, stream):
        # Read stream `i` frames in daemon thread
        n, f = 0, self.frame # frame number, frame array
        while cap.isOpened() and n < f:
            n += 1
            success, im = cap.read()
            if success:
                self.img = np.expand_dims(im, axis=0)
            else:
                self.img = np.zeros_like(self.img)
                cap.open(stream)  # re-open stream if signal was lost
            time.sleep(0.0)  # wait time

    def __iter__(self):
        self.count = -1
        return self

    def __next__(self):
        self.count += 1
        #if not self.thread.is_alive() or cv2.waitKey(1) == ord('q'):  # q to quit
         #   cv2.destroyAllWindows()
          #  raise StopIteration
        success, img = self.cap.read()
        self.img = img
        im0 = self.img.copy()
        if self.transforms:
            im = np.stack(self.transforms(im0))  # transforms
        else:
            im = np.stack(letterbox(im0, self.img_size, stride=self.stride, auto=self.auto)[0])  # resize
            im = im.transpose((2, 0, 1))  # BGR to RGB, BHWC to BCHW
            im = np.ascontiguousarray(im)  # contiguous

        return im, im0

    def __len__(self):
        return 1e12  # 1E12 frames = 32 streams at 30 FPS for 30 years


def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)


if __name__=="__main__":
    loader = StreamLoader(0)

    while True:
        im, im0 = next(iter(loader))
        print(im.shape)
        print(im0.shape)