from pydantic import BaseModel
from typing import List


class Scene(BaseModel):
    voiceover: str
    visual: str
    duration: float


class Script(BaseModel):
    title: str
    scenes: List[Scene]


def generate_script(topic: str) -> Script:
    # Temporary deterministic logic (no API yet)
    return Script(
        title=f"{topic} Explained",
        scenes=[
            Scene(
                voiceover=f"{topic} is used in neural networks.",
                visual="simple neural network",
                duration=6.0,
            )
        ],
    )