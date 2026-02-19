from ultralytics import YOLO
from tqdm import tqdm
import zipfile
import random
import cv2
import os
import json
import shutil

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

def get_main_features_areas(img, filename):
    x,y,w,h,f = [],[],[],[],[]
    
    # separate objects that are on the title
    director_and_movie_title = filename.split('.')[0]
    movie_title = director_and_movie_title.split('__')[0]
    elements_from_title = movie_title.split(' ')
    
    priority_order = ["face", "person", "text"] + elements_from_title 
    
    # detect all possible generic objects
    model = YOLO("yolo26n.pt")
    results = model([img], verbose=False)
    objects = results[0].boxes
    for box in objects:
        curr_x = int(box.xyxy[0][0])
        curr_y = int(box.xyxy[0][1])
        curr_w = int(box.xyxy[0][2] - box.xyxy[0][0])
        curr_h = int(box.xyxy[0][3] - box.xyxy[0][1])
        class_name = model.names[int(box.cls[0])]
        if class_name not in priority_order:
            priority_order.append(class_name)
            
        x.append(curr_x)
        y.append(curr_y)
        w.append(curr_w)
        h.append(curr_h)
        f.append(class_name)
            
    # recongnize faces
    # TODO:
    
    # recognize text
    # TODO:
    
    # ordering features by priority
    features_with_priority = sorted(zip(x, y, w, h, f), key=lambda item: priority_order.index(item[4]) )
    x, y, w, h, f = zip(*features_with_priority) if features_with_priority else ([], [], [], [], []) 
    
    # print("Detected features (ordered by priority):")
    # for idx, feature in enumerate(f):
    #     print(f"Feature {idx+1}: {feature} at ({x[idx]}, {y[idx]}) with size ({w[idx]}, {h[idx]})")
        
    return x, y, w, h, f

def image_gen(image_path, outputs_path, zips_path):
    image = cv2.imread(image_path)
    if os.path.exists(outputs_path):
        shutil.rmtree(outputs_path)
    os.makedirs(outputs_path, exist_ok=True)
    
    original_filename_with_ext = image_path.split('/')[-1]
    original_filename_no_ext = original_filename_with_ext.split('.')[0]
    outputs_path = os.path.join(outputs_path, original_filename_no_ext)
    os.makedirs(outputs_path, exist_ok=True)
    
    xs, ys, widths, heights, features = get_main_features_areas(image, original_filename_with_ext)
    functions = [blur_rectangle, pixelated_rectangle, negative_rectangle]
    
    metadata = []
    MAX_FEATURES = 5
    curr_feature = len(features) if len(features) < MAX_FEATURES else MAX_FEATURES
    cv2.imwrite(f"{outputs_path}/hint{curr_feature+1}.png", image)
    for x, y, w, h, f in zip(xs, ys, widths, heights, features):
        if curr_feature <= 0:
            break
        func = functions[random.randint(0, len(functions)-1)]
        if func == negative_rectangle:
            functions = list(filter(lambda x: x != negative_rectangle, functions))
        hint_output_path = f"{outputs_path}/hint{curr_feature}.png"
        metadata.append({
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "feature": f,
            "func": func.__name__,
            "original_filename": original_filename_with_ext,
            "output_filename": hint_output_path,
            "times_played": 0,
            "times_hit": 0,
            "times_missed": 0,
        })
        
        image = func(image, x, y, w, h)
        cv2.imwrite(hint_output_path, image)
        curr_feature -= 1
        
    # zip the hints files together    
    os.makedirs(zips_path, exist_ok=True)
    with zipfile.ZipFile(f"{zips_path}/{original_filename_no_ext}.zip", 'w') as zipf:
        for file in os.listdir(outputs_path):
            zipf.write(os.path.join(outputs_path, file), file)
    
    with open(f"{outputs_path}/metadata.json", 'w') as f:
        json.dump(metadata, f, indent=4)
        
    # cv2.imshow('IMAGE', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":

    pngs_path = os.path.join('pngs')
    zips_path = os.path.join('zips')
    outputs_path = os.path.join('outputs')
    
    pngs = os.listdir(pngs_path)
    for png in tqdm(pngs):
        image_gen(os.path.join(pngs_path, png), outputs_path, zips_path)