from abc import ABC, abstractmethod
from pathlib import Path
import whisper


class Transcriber(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def transcribe(self, path) -> str:
        pass


class WhisperTranscriber(Transcriber):
    whisper_model_type: str = "large"

    def __init__(self, device: str | None):
        self.model = whisper.load_model(self.whisper_model_type, device=device)

    def transcribe(self, path: Path | str) -> str:
        transcription: str = self.model.transcribe(str(path))["text"]

        return transcription
