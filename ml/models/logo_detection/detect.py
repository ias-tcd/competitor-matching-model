import logging
import time
from pathlib import Path

import torch
from yolov7_package import Yolov7Detector
from yolov7_package.models.experimental import attempt_load
from yolov7_package.utils.datasets import LoadImages
from yolov7_package.utils.general import check_img_size, non_max_suppression, scale_coords, set_logging, xyxy2xywh
from yolov7_package.utils.torch_utils import TracedModel, select_device, time_synchronized

from .data import BoundingBox, LogoDetectionInference


class Detector:
    def __init__(
        self,
        weights,
        source,
        img_size=640,
        conf_thres=0.09,
        iou_thres=0.45,
        device="",
        view_img=False,
        save_txt=False,
        save_conf=False,
        nosave=False,
        classes=None,
        agnostic_nms=False,
        augment=False,
        update=False,
        project="",
        name="",
        exist_ok=False,
        no_trace=False,
    ):
        self.weights = weights
        self.source = source
        self.img_size = img_size
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.device = device
        self.view_img = view_img
        self.save_txt = save_txt
        self.save_conf = save_conf
        self.nosave = nosave
        self.classes = classes
        self.agnostic_nms = agnostic_nms
        self.augment = augment
        self.update = update
        self.project = project
        self.name = name
        self.exist_ok = exist_ok
        self.no_trace = no_trace

    def detect(self):
        source, weights, imgsz, trace = self.source, self.weights, self.img_size, self.no_trace

        # Initialize
        set_logging()
        device = select_device(self.device)
        half = device.type != "cpu"  # half precision only supported on CUDA

        # Load model
        model = self.load_model(weights, device, trace, half)

        # Get stride and imgsz
        stride, imgsz = self.get_stride_and_imgsz(model, imgsz)

        # Get dataset
        dataset = self.get_dataset(source, imgsz, stride)

        # Get names
        names = self.get_names(model)

        detection_inference = self.run_inference(model, device, imgsz, names, half, dataset)
        return detection_inference

    def load_model(self, weights, device, trace, half):
        Yolov7Detector(weights=weights, traced=False)
        model = attempt_load(weights, map_location=device)  # load FP32 model
        if trace:
            model = TracedModel(model, device, self.img_size)

        if half:
            model.half()  # to FP16
        return model

    def get_stride_and_imgsz(self, model, imgsz):
        stride = int(model.stride.max())  # model stride
        imgsz = check_img_size(imgsz, s=stride)  # check img_size
        return stride, imgsz

    def get_dataset(self, source, imgsz, stride):
        dataset = LoadImages(source, img_size=imgsz, stride=stride)
        return dataset

    def get_names(self, model):
        names = model.module.names if hasattr(model, "module") else model.names
        return names

    def run_inference(self, model, device, imgsz, names, half, dataset):
        inferences = []
        coordinates = []
        if device.type != "cpu":
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = time_synchronized()
            with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
                pred = model(img, augment=self.augment)[0]
            t2 = time_synchronized()

            # Apply NMS
            pred = non_max_suppression(
                pred, self.conf_thres, self.iou_thres, classes=self.classes, agnostic=self.agnostic_nms
            )
            t3 = time_synchronized()

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                p, s, im0 = path, "", im0s

                p = Path(p)  # to Path
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                    # print(f"BOXES ---->>>> {det[:, :4]}")

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):

                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh

                        # Store data into the classes
                        bbox_coordinates = BoundingBox(x=xywh[0], y=xywh[1], w=xywh[2], h=xywh[3])
                        inference = LogoDetectionInference(bounding_box=bbox_coordinates, confidence=conf.item())
                        inferences.append(inference)
                        coordinates.append(xyxy)

                logging.basicConfig()
                logger = logging.getLogger()
                logger.setLevel(logging.INFO)
                # Print time (inference + NMS)
                logger.info(f"{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS")

            for i, (c, inf) in enumerate(zip(coordinates, inferences)):
                for j, next_c in enumerate(coordinates):
                    if i != j:  # Prevent self-comparison
                        # Printing enumeration of boxes
                        print(i)
                        if self.check_box_containment(*c, *next_c):
                            inf.overlap= True
                        print(inf.overlap)


            logger.info(f"Done. ({time.time() - t0:.3f}s)")
            return inferences

    def check_box_containment(self, x1, y1, x2, y2, x3, y3, x4, y4):
            area1 = (x2 - x1) * (y2 - y1)

            x_intersection_start = max(x1, x3)
            y_intersection_start = max(y1, y3)
            x_intersection_end = min(x2, x4)
            y_intersection_end = min(y2, y4)

            intersection_area = max(0, x_intersection_end - x_intersection_start) * max(0,
                                                                                        y_intersection_end - y_intersection_start)
            percentage_contained = (intersection_area / area1) * 100
            print(percentage_contained)
            return percentage_contained >= 50
