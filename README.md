# 🎬 Frame Guesser

An interactive movie-frame guessing game built with **Django REST API + SvelteKit frontend**.

Players receive progressively clearer image hints, pick the correct movie/discipline option, and score points based on both difficulty and how quickly they answer.

---

## ✨ General overview of features

- User registration/login with JWT authentication
- Session-based gameplay with multiple frames per run
- Progressive hints per frame (request next hint anytime)
- Scoring based on hint usage + frame difficulty
- Leaderboard/home feed with users + feedback messages
- End-of-run report with points, accuracy, and average comparison
- Admin upload tools for frames (single batch or zip bundles)

## 🖼️ Frame generation pipeline (AI model)

The utility in `scripts/frames/image_gen.py` can generate multiple hint images from source frames by applying progressive visual transformations (blur/pixelate/negative) and exporting zip bundles.

High-level process:

- Detect key regions (YOLO11n ONNX)
    - It's the smallest model in the YOLO11 family — fast on CPU, low memory, and more than good enough to spot the dominant subjects in a movie still.
    - Inference goes through `cv2.dnn.readNetFromONNX` with the CPU target. That means the *only* runtime dependency for hint generation is OpenCV (`opencv-contrib-python-headless`) — no `torch`, no `ultralytics`, no CUDA drivers. Keeps the backend image small and portable.
- Apply obfuscation progressively on detected regions

This script is used by Staff members in a dedicated page to onboard movies without touching the CLI.

- Log in as a staff account directly on the page.
- Upload a source image and use the built-in 400×400 cropper (drag + zoom) to frame it.
- Click **GENERATE HINTS** — the backend runs the image through the AI pipeline described above and streams the hint set back for preview.
- It is possible to **REGENERATE HINTS** to run the pipeline again on the same crop.
- The rest of the details such as name, year and director are typed by the user and then saved.
- The same page also lists all existing movies in list or grid view, with search and difficulty/hint-count badges, to avoid adding duplicate movies.

## 📸 Screenshots

![alt text](screenshot2.png)

![alt text](screenshot1.png)