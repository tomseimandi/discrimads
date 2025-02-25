"""
Extract infos from tiktok videos.
"""

import os
import torch
from discrimads.download import download_video
from discrimads.extract_audio import extract_audio
from discrimads.gender_audio import get_gender_for_audio
from discrimads.transcription import WhisperTranscriber
from discrimads.util import VideoContent


def extract_content_from_video(url: str) -> VideoContent:
    video_path = "tmp/video.mp4"
    audio_path = "tmp/audio.mp3"

    if not os.path.exists(video_path):
        download_video(url=url, video_path=video_path)
    if not os.path.exists(audio_path):
        extract_audio(video_path, audio_path, duration=1)
    # torch device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # get gender
    gender = get_gender_for_audio(
        audio_path,
        device=device,
    )
    # get transcription
    transcriber = WhisperTranscriber(device=device)
    audio_text = transcriber.transcribe(path=audio_path)

    content = VideoContent(
        url=url,
        audio_text=audio_text,
        audio_gender=gender,
        audio_jobs=[],  # TODO: implement
    )
    return content


if __name__ == "__main__":
    extract_content_from_video(url=1)
