from ultralytics import YOLO
import random
import cv2
import os
import json

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

def calculate_overlap(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    interArea = max(0, xB - xA) * max(0, yB - yA)
    
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    
    iou = interArea / float(boxAArea + boxBArea - interArea) if (boxAArea + boxBArea - interArea) > 0 else 0
    return iou

def get_main_features_areas(img, filename):
    x,y,w,h,f = [],[],[],[],[]
    
    # separate objects that are on the title
    # director_and_movie_title = filename.split('.')[0]
    # movie_title = director_and_movie_title.split('__')[0]
    # elements_from_title = movie_title.split(' ')
    elements_from_title = []
    
    priority_order = ["face", "person", "text"] + elements_from_title 
    OVERLAP_THRESHOLD = 0 # in percentage of area
    
    # detect all possible generic objects
    model = YOLO("yolo26n.pt")
    results = model([img])
    objects = results[0].boxes
    for box in objects:
        curr_x = int(box.xyxy[0][0])
        curr_y = int(box.xyxy[0][1])
        curr_w = int(box.xyxy[0][2] - box.xyxy[0][0])
        curr_h = int(box.xyxy[0][3] - box.xyxy[0][1])
        class_name = model.names[int(box.cls[0])]
        if class_name not in priority_order:
            priority_order.append(class_name)
            
        # try to merge boxes of same class that are close to each other
        if class_name in f:
            merged = False
            for idx, existing_class in enumerate(f):
                if existing_class != class_name:
                    continue
                
                overlap = calculate_overlap(
                    (x[idx], y[idx], x[idx]+w[idx], y[idx]+h[idx]),
                    (curr_x, curr_y, curr_x+curr_w, curr_y+curr_h)
                )
                print(OVERLAP_THRESHOLD, overlap)
                
                if overlap >= OVERLAP_THRESHOLD:
                    merged = True
                    x[idx] = min(x[idx], curr_x)
                    y[idx] = min(y[idx], curr_y)
                    w[idx] = max(x[idx] + w[idx], curr_x + curr_w) - x[idx]
                    h[idx] = max(y[idx] + h[idx], curr_y + curr_h) - y[idx]
                    break
            if not merged:
                x.append(curr_x)
                y.append(curr_y)
                w.append(curr_w)
                h.append(curr_h)
                f.append(class_name)
        else:
            x.append(curr_x)
            y.append(curr_y)
            w.append(curr_w)
            h.append(curr_h)
            f.append(class_name)
            
    # recongnize faces
    
    # recognize text
    
    # ordering features by priority
    features_with_priority = sorted(zip(x, y, w, h, f), key=lambda item: priority_order.index(item[4]) )
    x, y, w, h, f = zip(*features_with_priority) if features_with_priority else ([], [], [], [], []) 
    
    print("Detected features (ordered by priority):")
    for idx, feature in enumerate(f):
        print(f"Feature {idx+1}: {feature} at ({x[idx]}, {y[idx]}) with size ({w[idx]}, {h[idx]})")
        
    return x, y, w, h, f


if __name__ == "__main__":
    image_path = 'test2.png' 
    image = cv2.imread(image_path)
    os.makedirs('output', exist_ok=True)
    original_filename = image_path.split('/')[-1]
    
    xs, ys, widths, heights, features = get_main_features_areas(image, original_filename)
    # functions = [blur_rectangle, pixelated_rectangle, negative_rectangle]
    functions = [blur_rectangle]
    
    metadata = []
    MAX_FEATURES = 2
    curr_feature = len(features) if len(features) < MAX_FEATURES else MAX_FEATURES
    cv2.imwrite(f"output/hint{curr_feature+1}.png", image)
    for x, y, w, h, f in zip(xs, ys, widths, heights, features):
        if curr_feature <= 0:
            break
        func = functions[random.randint(0, len(functions)-1)]
        if func == negative_rectangle:
            functions = list(filter(lambda x: x != negative_rectangle, functions))
        output_path = f"output/hint{curr_feature}.png"
        metadata.append({
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "feature": f,
            "func": func.__name__,
            "original_filename": original_filename,
            "output_filename": output_path,
            "times_played": 0,
            "times_hit": 0,
            "times_missed": 0,
        })
        
        image = func(image, x, y, w, h)
        cv2.imwrite(output_path, image)
        curr_feature -= 1
        
    with open('output/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)
        
    # cv2.imshow('IMAGE', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()