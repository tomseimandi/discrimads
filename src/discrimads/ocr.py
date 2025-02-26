"""OCR functions."""
import pytesseract
from pathlib import Path
import os


def ocr(frame_path: str):
    """OCR a frame to text and/or image."""
    text = pytesseract.image_to_string(frame_path)
    return text.strip()


def get_text(frames_dir: Path) -> str:
    paths = os.listdir(frames_dir)
    """Extract text from list of frames extracted from a video."""
    previous_text = ""
    texts = []
    for path in paths:
        text = ocr(path)
        if text == "":
            continue
        elif text == previous_text:
            continue
        previous_text = text
        texts.append(text)
    return " ".join(texts)
