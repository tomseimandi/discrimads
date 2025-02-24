"""Extract audio from url using ffmpeg."""
import subprocess


def extract_audio(url, output_audio="output.mp3"):
    """Extracts audio from a video URL using ffmpeg."""
    command = [
        "ffmpeg",
        "-i", url,       # Input video URL
        "-q:a", "0",      # Highest audio quality
        "-map", "a",      # Extract only the audio stream
        output_audio      # Output audio file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Audio extracted successfully: {output_audio}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")


if __name__ == "__main__":
    extract_audio("https://example.com/video.mp4", "audio.mp3")
