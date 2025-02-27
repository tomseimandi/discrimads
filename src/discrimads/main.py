"""
Extract infos from tiktok videos.
"""

import pandas as pd
import os
import torch
from discrimads.download import download_video
from discrimads.extract_audio import extract_audio
from discrimads.gender_audio import get_gender_for_audio
from discrimads.transcription import WhisperTranscriber
from discrimads.util import VideoContent
from discrimads.extract_frames import extract_frames
from discrimads.ocr import get_text
# from discrimads.classify import predict_gender
from tqdm import tqdm


def extract_content_from_urls(urls: list[str]) -> pd.DataFrame:
    contents = []
    for i, url in tqdm(enumerate(urls)):
        video_path = f"tmp/video_{i}.mp4"
        audio_path = f"tmp/audio_{i}.mp3"

        if not os.path.exists(video_path):
            download_video(url=url, video_path=video_path)
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
            url=url,
            audio_text=audio_text,
            audio_gender=gender,
            audio_jobs=[],  # TODO: implement
            ocr_text=text,
            frames_gender=0  # TODO: implement
        )
        contents.append(content)

    df = pd.DataFrame.from_records([content.model_dump() for content in contents])
    df.to_parquet("data/sample_content.parquet")
    return df


if __name__ == "__main__":
    # load tiktok data
    df = pd.read_parquet("data/tiktok_sample.parquet")
    # get urls
    urls = [video_list[0]["url"] for video_list in df.videos]

    # extract content
    extract_content_from_urls(urls=urls)
