"""Util."""

from dataclasses import dataclass
from enum import Enum


class AudioGender(Enum):
    MAN = "man"
    WOMAN = "woman"
    BOTH = "both"
    NO_VOICE = "no voice"


@dataclass
class VideoContent():
    url: str
    audio_text: str
    audio_gender: AudioGender
    audio_jobs: list[str]
    ocr_text: str
    frames_gender: int

    def model_dump(self):
        return {
            "url": self.url,
            "audio_text": self.audio_text,
            "audio_gender": self.audio_gender.value,
            "audio_jobs": self.audio_jobs,
            "ocr_text": self.ocr_text,
            "frames_gender": self.frames_gender
        }


def flatten_ad_dict(ad_dict: dict):
    """
    Flatten dictionary on top level.
    """
    flat_dict = {}
    for k, v in ad_dict.items():
        if not isinstance(v, dict):
            flat_dict[k] = v
        else:
            flat_dict.update(v)
    return flat_dict
