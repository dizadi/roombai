
from models.common import DetectMultiBackend
from utils.general import (cv2, non_max_suppression, scale_boxes)
from utils.plots import Annotator, colors
from utils.torch_utils import smart_inference_mode
import torch
from pathlib import Path

class DetectorWrapper:
    def __init__(
        self,
        weights_path='yolov5/yolov5s.pt',
        imgsz=(640,640),
        classes=[],  # filter by class: --class 0, or --class 0 2 3
        conf_thres=0.4,
        iou_thres=0.25,
        max_det=500,
        agnostic_nms=False,  # class-agnostic NMS
        line_thickness=3,  # bounding box thickness (pixels)
    ):
        self._model = DetectMultiBackend(weights_path)
        self._stride, self._names, self._pt = self._model.stride, self._model.names, self._model.pt
        self._line_thickness = line_thickness
        self._conf_thres = conf_thres
        self._classes = classes
        self._max_det = max_det
        self._iou_thres = iou_thres
        self._agnostic_nms = agnostic_nms
        self._model.warmup(imgsz=(1 if self._pt or self._model.triton else 1, 3, *imgsz))  # warmup
    
    def detect(self, im):
        im = self.preprocess(im)
        # Inference
        pred = self._model(im)
        pred = non_max_suppression(pred, self._conf_thres, self._iou_thres, self._classes, self._agnostic_nms, max_det=self._max_det)
        return pred

    def preprocess(
        self,
        im,
    ):
        im = torch.from_numpy(im).to(self._model.device)
        im = im.half() if self._model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim 
        return im

    def save_annotated_frame(self, im, im0, pred, save_path):
        annotated_img = self.annotate_frame(im, im0, pred)
        self.save_frame(annotated_img, save_path)
    
    def interpret_predictions(self, pred):
        classifications, confidences, bboxes = [], [], []
        for i, det in enumerate(pred):
            if len(det):
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    classifications.append(self._names[c])
                    confidences.append(conf)
                    bboxes.append(xyxy)
        return classifications, confidences, bboxes


    def annotate_frame(self, im, im0, pred):
        annotator = Annotator(im0, line_width=self._line_thickness, example=str(self._names))
        for i, det in enumerate(pred): 
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[1:], det[:, :4], im0.shape).round()
                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    label = (f'{self._names[c]} {conf:.2f}')
                    annotator.box_label(xyxy, label, color=colors(c, True))
            # Stream results
        annotated_img = annotator.result()
        return annotated_img

    def save_frame(self, annotated_frame, save_path='test.jpg'):
        print(f'image saved at {save_path}')
        cv2.imwrite(save_path, annotated_frame)
    
    def show_annotated_frame(self, im, im0, pred):
        annotated_frame = self.annotate_frame(im, im0, pred)
        cv2.imshow('frame',annotated_frame)
        cv2.waitKey(1)


from dataloader import StreamLoader
import time
import numpy as np

if __name__=="__main__":
    loader = StreamLoader(0) #take webcam
    img, im0 = next(iter(loader))
    model_wrapper = DetectorWrapper()
    pred = model_wrapper.detect(img)
    model_wrapper.show_annotated_frame(img, im0, pred)