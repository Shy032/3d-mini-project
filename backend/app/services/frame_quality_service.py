from __future__ import annotations

from pathlib import Path
import numpy as np


def evaluate_frame(image_path: Path) -> dict:
    warnings: list[str] = []

    gray = None
    brightness = 0.5
    blur_score = 80.0

    try:
        import cv2  # type: ignore

        img = cv2.imread(str(image_path))
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            brightness = float(gray.mean() / 255.0)
    except Exception:
        from PIL import Image

        with Image.open(image_path) as im:
            arr = np.array(im.convert("L"), dtype=np.float32)
            gray = arr
            brightness = float(arr.mean() / 255.0)
            gx = np.diff(arr, axis=1, prepend=arr[:, :1])
            gy = np.diff(arr, axis=0, prepend=arr[:1, :])
            blur_score = float(np.mean(gx * gx + gy * gy))

    if blur_score < 60:
        warnings.append("Image too blurry")
        warnings.append("Move slower")
    if brightness < 0.25:
        warnings.append("Too dark")
    if gray is not None and gray.shape[0] < 480:
        warnings.append("Low resolution frame")

    accepted = len([w for w in warnings if w in {"Image too blurry", "Too dark"}]) == 0
    return {
        "blur_score": round(blur_score, 2),
        "brightness": round(brightness, 3),
        "warnings": warnings,
        "accepted": accepted,
    }
