import os
import sys
import tempfile
from pathlib import Path

import cv2  # type: ignore

_CONTAINER_SCRIPTS = Path("/scripts/frames")
_REPO_SCRIPTS = Path(__file__).resolve().parents[4] / "scripts" / "frames"
SCRIPTS_DIR = _CONTAINER_SCRIPTS if _CONTAINER_SCRIPTS.is_dir() else _REPO_SCRIPTS


def generate_hints(image_bytes: bytes, extension: str = "png") -> list[bytes]:
    if not SCRIPTS_DIR.is_dir():
        raise RuntimeError(f"Scripts folder not found at {SCRIPTS_DIR}")

    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))

    from image_gen import generate_images  # type: ignore 

    ext = (extension or "png").lower().lstrip(".")

    with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    try:
        frames = generate_images(tmp_path)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    hints: list[bytes] = []
    for frame in reversed(frames):
        success, buf = cv2.imencode(".png", frame)
        if not success:
            raise RuntimeError("Failed to encode generated hint as PNG")
        hints.append(buf.tobytes())

    return hints
