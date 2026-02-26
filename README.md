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
- Detect key regions with YOLO
- Apply obfuscation progressively
- Export ordered hint images + metadata

## 📸 Screenshots

![alt text](screenshot2.png)

![alt text](screenshot1.png)