import os
import requests
from pathlib import Path


def download_video(url, video_path):
    """Downloads a video from a URL and saves it to a local file."""
    video_path = Path(video_path)

    # Create parent directory if it doesn't exist
    if not video_path.parent.exists():
        os.makedirs(video_path.parent)

    # Stream the file download to prevent memory overload
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(video_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                file.write(chunk)
        print(f"Download complete: {video_path}")
    else:
        print(f"Failed to download video. HTTP Status Code: {response.status_code}")
