"""Extract frames from video"""
from pathlib import Path
import os
import cv2


def extract_frames(video_path: str) -> Path:
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_number = 0
    frame_skip = 30
    saved_frame_count = 0

    # output path
    output_path = Path(video_path).parent / "frames"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    while True:
        ret, frame = capture.read()
        if not ret:
            break
        if frame_number % frame_skip == 0:
            frame_filename = output_path, f"frame_{saved_frame_count}.jpg"
            try:
                cv2.imwrite(frame_filename, frame)
                saved_frame_count += 1
            except Exception as e:
                print(f"Error saving frame: {e}")
        frame_number += 1
    capture.release()
    return output_path
