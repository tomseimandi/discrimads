"""Util"""

from dataclasses import dataclass
from enum import Enum


@dataclass
class AudioGender(Enum):
    MAN = "man"
    WOMAN = "woman"
    BOTH = "both"
    NO_VOICE = "no voice"


@dataclass
class VideoContent:
    url: str
    audio_text: str
    audio_gender: AudioGender
    audio_jobs: list[str]
