"""Extract audio from url using ffmpeg."""

import subprocess


def extract_audio(
    file, output_audio: str = "output.mp3", start: int = 0, duration: int = 5
) -> str:
    """Extracts audio from a video file using ffmpeg."""
    command = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "debug",
        "-i",
        file,  # Input video file
        "-q:a",
        "0",  # Highest audio quality
        "-map",
        "a",  # Extract only the audio stream
        "-c:a",
        "mp3",
        "-ss",
        str(start),
        "-t",
        str(duration),
        output_audio,
    ]

    try:
        _ = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"Audio extracted successfully: {output_audio}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
    return output_audio
