import os
# import numpy as np
import shutil
import sys
# import argparse
import time
from pathlib import Path

import cv2
import gradio as gr
import torch
import torch.backends.cudnn as cudnn
from numpy import random
from PIL import Image

# import pandas as pd


BASE_DIR = os.curdir
os.chdir(BASE_DIR)
os.makedirs(f"{BASE_DIR}/input", exist_ok=True)
# os.system(f"git clone https://github.com/WongKinYiu/yolov7.git {BASE_DIR}/yolov7")
sys.path.append(f"{BASE_DIR}/yolov7")
# os.system("pip install yolov7-package==0.0.12")


def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def detect(opt, save_img=False):
    #     from models.experimental import attempt_load
    #     from utils.datasets import LoadStreams, LoadImages
    #     from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    #         scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
    #     from utils.plots import plot_one_box
    #     from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

    print(f"Options: {opt}")

    from yolov7_package import Yolov7Detector
    from yolov7_package.models.experimental import attempt_load
    from yolov7_package.utils.datasets import LoadImages, LoadStreams
    from yolov7_package.utils.general import (
        apply_classifier,
        check_img_size,
        check_imshow,
        check_requirements,
        increment_path,
        non_max_suppression,
        scale_coords,
        set_logging,
        strip_optimizer,
        xyxy2xywh,
    )
    from yolov7_package.utils.torch_utils import TracedModel, load_classifier, select_device, time_synchronized

    bbox = {}
    source, weights, view_img, save_txt, imgsz, trace = (
        opt.source,
        opt.weights,
        opt.view_img,
        opt.save_txt,
        opt.img_size,
        not opt.no_trace,
    )
    save_img = not opt.nosave and not source.endswith(".txt")  # save inference images
    webcam = (
        source.isnumeric()
        or source.endswith(".txt")
        or source.lower().startswith(("rtsp://", "rtmp://", "http://", "https://"))
    )

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    (save_dir / "labels" if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(opt.device)
    half = device.type != "cpu"  # half precision only supported on CUDA

    # Load model
    det = Yolov7Detector(weights=weights, traced=False)
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    if trace:
        model = TracedModel(model, device, opt.img_size)

    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name="resnet101", n=2)  # initialize
        modelc.load_state_dict(torch.load("weights/resnet101.pt", map_location=device)["model"]).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, "module") else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != "cpu":
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Warmup
        if device.type != "cpu" and (
            old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]
        ):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                model(img, augment=opt.augment)[0]

        # Inference
        t1 = time_synchronized()
        with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
            pred = model(img, augment=opt.augment)[0]
        t2 = time_synchronized()

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        t3 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], "%g: " % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, "", im0s, getattr(dataset, "frame", 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # img.jpg
            txt_path = str(save_dir / "labels" / p.stem) + ("" if dataset.mode == "image" else f"_{frame}")  # img.txt
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                #                 print(f"BOXES ---->>>> {det[:, :4]}")
                bbox[f"{txt_path.split('/')[4]}"] = (det[:, :4]).numpy()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                print(f"Det: {det}")
                print(f"GN: {gn}")
                print(f"Reversed: {reversed(det)}")
                if save_txt:
                    with open(txt_path + ".txt", "a") as f:
                        f.write("cls\t|x2-x1|/2\t|y2-y1|/2\tw\t\t\th\t\t\tconf\n")
                for *xyxy, conf, cls in reversed(det):
                    print(f"xyxy: {xyxy}")
                    print(f"Conf: {conf}")
                    print(f"cls: {cls}")

                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        print(f"Normalised xywh: {xywh}")
                        line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + ".txt", "a") as f:
                            line = ("%g " * len(line)).rstrip() % line + "\n"
                            line = line.replace(" ", "\t")
                            f.write(line)

                    if save_img or view_img:  # Add bbox to image
                        label = f"{names[int(cls)]} {conf:.2f}"
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

            # Print time (inference + NMS)
            print(f"{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS")

            # Stream results
            # if view_img:
            #     cv2.imshow(str(p), im0)
            #     cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == "image":
                    # Image.fromarray(im0).show()
                    cv2.imwrite(save_path, im0)
                    print(f" The image with the result is saved in: {save_path}")
                # else:  # 'video' or 'stream'
                #     if vid_path != save_path:  # new video
                #         vid_path = save_path
                #         if isinstance(vid_writer, cv2.VideoWriter):
                #             vid_writer.release()  # release previous video writer
                #         if vid_cap:  # video
                #             fps = vid_cap.get(cv2.CAP_PROP_FPS)
                #             w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                #             h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                #         else:  # stream
                #             fps, w, h = 30, im0.shape[1], im0.shape[0]
                #             save_path += '.mp4'
                #         vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                #     vid_writer.write(im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ""
        # print(f"Results saved to {save_dir}{s}")

    print(f"Done. ({time.time() - t0:.3f}s)")
    return bbox, save_path


class options:
    def __init__(
        self,
        weights,
        source,
        img_size=640,
        conf_thres=0.1,
        iou_thres=0.45,
        device="",
        view_img=False,
        save_txt=True,
        save_conf=True,
        nosave=False,
        classes=None,
        agnostic_nms=False,
        augment=False,
        update=False,
        project="runs/detect",
        name="exp",
        exist_ok=False,
        no_trace=True,
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

    def __str__(self):
        return (
            f"self.weights={self.weights}\n"
            f"self.source={self.source}\n"
            f"self.img_size={self.img_size}\n"
            f"self.conf_thres={self.conf_thres}\n"
            f"self.iou_thres={self.iou_thres}\n"
            f"self.device={self.device}\n"
            f"self.view_img={self.view_img}\n"
            f"self.save_txt={self.save_txt}\n"
            f"self.save_conf={self.save_conf}\n"
            f"self.nosave={self.nosave}\n"
            f"self.classes={self.classes}\n"
            f"self.agnostic_nms={self.agnostic_nms}\n"
            f"self.augment={self.augment}\n"
            f"self.update={self.update}\n"
            f"self.project={self.project}\n"
            f"self.name={self.name}\n"
            f"self.exist_ok={self.exist_ok}\n"
            f"self.no_trace={self.no_trace}"
        )


def get_output(input_image, folder_name="exp", trace=False):
    ### Numpy -> PIL
    # input_image = Image.fromarray(input_image).convert('RGB')
    # input_image.save(f"{BASE_DIR}/input/image.jpg")
    source = f"{BASE_DIR}/input"
    opt = options(weights="logo_detection.pt", source=source, name=folder_name, no_trace=not trace)
    bbox = None
    with torch.no_grad():
        bbox, output_path = detect(opt)
    if os.path.exists(output_path):
        return Image.open(output_path)
    else:
        return input_image


def my_test(trace):
    if trace:
        exte = "time-trace-2"
    else:
        exte = "time-no-trace-2"
    print(BASE_DIR)
    timings = {}
    for dir in os.listdir(f"{BASE_DIR}/input"):
        print("looping")
        print(dir)
        if dir.endswith(".jpg"):
            print("Exiting")
            continue
        timings[dir] = []
        print("Entering inner loop")
        for subdir in os.listdir(f"{BASE_DIR}/input/{dir}"):
            print("inner looping")
            print(subdir)
            shutil.copy(f"{BASE_DIR}/input/{dir}/{subdir}", f"{BASE_DIR}/input/image.jpg")
            start = time.time()
            get_output(None, dir + "time-no-trace", trace)
            end = time.time()
            timings[dir].append(end - start)

    total_time = 0
    count = 0
    for brand, b_timings in timings.items():
        print(f"Timings for {brand}: total: {sum(b_timings)}, avg: {sum(b_timings) / len(b_timings)}")
        total_time += sum(b_timings)
        count += len(b_timings)
    print(f"Total timings: total: {total_time}, avg: {total_time / count}")


def perform_demo(args):
    image_path = args[0]
    trace = any(a for a in args if a == "trace")
    timings = any(a for a in args if a == "time")
    shutil.copy(f"{BASE_DIR}/{image_path}", f"{BASE_DIR}/input/")
    start_time = time.time()
    print("Starting")
    get_output(None, trace=trace)
    end_time = time.time()
    if timings:
        print(f"Time taken: {end_time - start_time}s")


if __name__ == "__main__":
    args = sys.argv
    if args and args[1] == "run":
        demo = gr.Interface(fn=get_output, inputs="image", outputs="image")
        demo.launch(debug=True)
    else:
        perform_demo(args[1:])

# 578 * 742
# (249, 361), (409, 361)
# (249, 472), (409, 472)
# w: 160
# h: 110
