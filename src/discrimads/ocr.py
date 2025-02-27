"""OCR functions."""
import pytesseract
from pathlib import Path
import os


def ocr(frame_path: str):
    """OCR a frame to text and/or image."""
    text = pytesseract.image_to_string(frame_path, lang="fra", config="--oem 1 --psm 6 -c textord_min_linesize=2.5 tessedit_do_invert=1")
    text = text.replace("\n", "")
    return text.strip()


def get_text(frames_dir: Path) -> str:
    """Extract text from list of frames extracted from a video."""
    paths = os.listdir(frames_dir)
    paths = filter(lambda x: x.endswith(".jpg"), paths)
    paths = list(map(lambda x: frames_dir / x, paths))

    previous_text = ""
    texts = []
    for path in paths:
        text = ocr(str(path))
        if text == "":
            continue
        elif text == previous_text:
            continue
        previous_text = text
        texts.append(text)
    return " ".join(texts)
