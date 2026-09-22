# from ultralytics import YOLO
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
    
    # detect all possible generic objects
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (_, saliencyMap) = saliency.computeSaliency(img)
    saliencyMap = (saliencyMap * 255).astype("uint8")
    _, thresh = cv2.threshold(saliencyMap, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for idx, cnt in enumerate(contours):
        curr_x, curr_y, curr_w, curr_h = cv2.boundingRect(cnt)
        if curr_w < 50 or curr_h < 50:
            continue
        x.append(curr_x)
        y.append(curr_y)
        w.append(curr_w)
        h.append(curr_h)
        f.append(f"{idx + 1}")
            
    # recongnize faces
    # TODO:
    
    # recognize text
    # TODO:
    
    return x, y, w, h, f

def generate_images(image_path: str)->list:
    print("="*50)
    print(f"Processing image: {image_path}")
    print("="*50)
    
    image = cv2.imread(image_path)
    image = cv2.resize(image, (400, 400))
    
    original_filename_with_ext = image_path.split('/')[-1]
    xs, ys, widths, heights, features = get_main_features_areas(image, original_filename_with_ext)
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