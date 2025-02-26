"""
Extract infos from tiktok videos.
"""

import pandas as pd
from pathlib import Path
import os
import torch
from discrimads.extract_audio import extract_audio
from discrimads.gender_audio import get_gender_for_audio
from discrimads.transcription import WhisperTranscriber
from discrimads.util import VideoContent
from discrimads.extract_frames import extract_frames
from discrimads.ocr import get_text
# from discrimads.classify import predict_gender
from tqdm import tqdm


def extract_content(paths: list[str]) -> pd.DataFrame:
    contents = []
    for i, video_path in tqdm(enumerate(paths)):
        audio_path = str(video_path).replace("mp4", "mp3")

        if not os.path.exists(audio_path):
            extract_audio(video_path, audio_path, duration=20)
        print(f"Video and audio {i} extracted.")

        # torch device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # get gender
        print("Processing audio.")
        gender = get_gender_for_audio(
            audio_path,
            device=device,
        )
        # get transcription
        transcriber = WhisperTranscriber(device=device)
        audio_text = transcriber.transcribe(path=audio_path)

        # get frames
        print("Processing video.")
        frames_dir = extract_frames(video_path=video_path)
        # ocr
        text = get_text(frames_dir)
        # classification from frames
        # frames_gender = predict_gender(frames_dir)

        content = VideoContent(
            url=str(video_path),
            audio_text=audio_text,
            audio_gender=gender,
            audio_jobs=[],  # TODO: implement
            ocr_text=text,
            frames_gender=0  # TODO: implement
        )
        contents.append(content)

    df = pd.DataFrame.from_records([content.model_dump() for content in contents])
    df.to_parquet("data/meta_content.parquet")
    return df


if __name__ == "__main__":
    # get paths
    paths = os.listdir("ads")
    paths = filter(lambda x: x.endswith(".mp4"), paths)
    paths = list(map(lambda x: Path("ads") / x, paths))

    # extract content
    extract_content(paths=paths)
