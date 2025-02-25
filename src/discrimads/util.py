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
