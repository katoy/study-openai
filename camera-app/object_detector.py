import cv2
import logging
from ultralytics import YOLO
from suppress_output import suppress_output

logging.getLogger("ultralytics").setLevel(logging.ERROR)

class ObjectDetector:
    """YOLOモデルを使用してカメラ映像から物体を検出し、ラベルと枠を描画するクラス"""

    def __init__(self, model_path="yolov9s.pt"):
        self.model = YOLO(model_path)

    def detect_objects(self, frame):
        """フレームからオブジェクトを検出"""
        with suppress_output():
            results = self.model(frame)
        return [(result.names[int(box.cls[0])], box.xyxy[0].tolist()) for result in results for box in result.boxes]

    def draw_boxes(self, frame, detections):
        """検出したオブジェクトに枠を描画"""
        for label, bbox in detections:
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
