import os
import random
import urllib.request  # type: ignore

import cv2  # type: ignore
from django.conf import settings  # type: ignore
from tqdm import tqdm


def blur_rectangle(img, x, y, w, h, blur_strength=101):
    roi = img[y:y+h, x:x+w]
    ksize = (blur_strength, blur_strength)
    blurred_roi = cv2.GaussianBlur(roi, ksize, 0)
    img[y:y+h, x:x+w] = blurred_roi
    return img
        
def pixelated_rectangle(img, x, y, w, h, pixel_resolution=15):
    roi = img[y:y+h, x:x+w]
    block_h = max(1, int(h * (pixel_resolution / w)))
    small = cv2.resize(roi, (pixel_resolution, block_h), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    img[y:y+h, x:x+w] = pixelated
    return img
        
def negative_rectangle(img, x, y, w, h, negative_strength=1):
    roi = img[y:y+h, x:x+w]
    negative_roi = cv2.bitwise_not(roi)
    blended_roi = cv2.addWeighted(roi, 1 - negative_strength, negative_roi, negative_strength, 0)
    img[y:y+h, x:x+w] = blended_roi
    return img

def get_main_features_areas(img, conf_thresh=0.25, nms_thresh=0.45, max_boxes=5):
    YOLO_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolo11n.onnx")
    net = cv2.dnn.readNetFromONNX(YOLO_FILE_PATH)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    h_orig, w_orig = img.shape[:2]

    # Preprocessing: 640x640 letterbox tensor normalized to [0, 1]
    blob = cv2.dnn.blobFromImage(img, 1.0 / 255.0, (640, 640), swapRB=True, crop=False)
    net.setInput(blob)
    output = net.forward()  # Shape: (1, 84, 8400)

    # Transpose to (8400, 84): rows are candidate boxes, cols are [x, y, w, h, class_scores...]
    preds = output[0].T

    boxes = []
    confidences = []
    scale_x = w_orig / 640.0
    scale_y = h_orig / 640.0

    for row in preds:
        # Check all 80 class scores at once
        class_scores = row[4:]
        _, max_score, _, _ = cv2.minMaxLoc(class_scores)

        # If any object type is detected with sufficient confidence
        if max_score >= conf_thresh:
            cx, cy, w, h = row[0], row[1], row[2], row[3]
            x = int((cx - 0.5 * w) * scale_x)
            y = int((cy - 0.5 * h) * scale_y)
            width = int(w * scale_x)
            height = int(h * scale_y)

            boxes.append([x, y, width, height])
            confidences.append(float(max_score))

    if not boxes:
        return [], [], [], [], []

    # Non-Maximum Suppression to merge overlapping boxes into a single target
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_thresh, nms_thresh)

    detected = []
    if len(indices) > 0:
        for idx in indices.flatten():
            bx, by, bw, bh = boxes[idx]
            # Clip bounds to image canvas
            bx = max(0, bx)
            by = max(0, by)
            bw = min(w_orig - bx, bw)
            bh = min(h_orig - by, bh)
            detected.append((bx, by, bw, bh))

    # Sort boxes by area descending (largest visual subjects first)
    detected = sorted(detected, key=lambda b: b[2] * b[3], reverse=True)[:max_boxes]

    xs = [b[0] for b in detected]
    ys = [b[1] for b in detected]
    ws = [b[2] for b in detected]
    hs = [b[3] for b in detected]
    fs = [f"object_{i+1}" for i in range(len(detected))]

    return xs, ys, ws, hs, fs

def generate_images(image_path: str)->list:
    print("="*50)
    print(f"Processing image: {image_path}")
    print("="*50)
    
    image = cv2.imread(image_path)
    image = cv2.resize(image, (400, 400))
    
    original_filename_with_ext = image_path.split('/')[-1]
    xs, ys, widths, heights, features = get_main_features_areas(image)
    functions = [blur_rectangle, pixelated_rectangle, negative_rectangle]
    
    metadata = []
    MAX_FEATURES = 5
    curr_feature = min(MAX_FEATURES, len(features))
    new_images = [image.copy()]
    for x, y, w, h, f in zip(xs, ys, widths, heights, features):
        if curr_feature <= 0:
            break

        func = functions[random.randint(0, len(functions)-1)]
        
        # negative function can be used only once
        if func == negative_rectangle:
            functions = list(filter(lambda x: x != negative_rectangle, functions))

        metadata.append({
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "feature": f,
            "func": func.__name__,
            "original_filename": original_filename_with_ext
        })
        
        image = func(image, x, y, w, h)
        new_images.append(image.copy())
        curr_feature -= 1    
    
    print(metadata)
    
    print("="*50)
    print(f"Finished processing image: {image_path}. A total of {len(new_images)} images were generated.")
    print("="*50, end="\n\n")
    
    return new_images

if __name__ == "__main__":

    input_path = os.path.join('pngs')
    input_images = os.listdir(input_path)
    for png in tqdm(input_images):
        generated_images = generate_images(os.path.join(input_path, png))
        
        for image in generated_images:
            cv2.imshow('IMAGE', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()