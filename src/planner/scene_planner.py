from pydantic import BaseModel
from typing import List
from enum import Enum


class VisualType(str, Enum):
    TEXT = "text"
    NEURAL_NETWORK = "neural_network"
    EQUATION = "equation"
    CODE = "code"


class Scene(BaseModel):
    voiceover: str
    visual: VisualType
    duration: float
    layers: List[int] | None = None  # for neural networks


class Script(BaseModel):
    title: str
    scenes: List[Scene]


def generate_script(topic: str) -> Script:
    """
    Deterministic dynamic script generator.
    For now, neural network layer sizes are hardcoded.
    Later LLM will generate these dynamically.
    """

    return Script(
        title=f"{topic} Explained",
        scenes=[
            Scene(
                voiceover=f"{topic} uses a neural network structure.",
                visual=VisualType.NEURAL_NETWORK,
                duration=6.0,
                layers=[3, 4, 2],  # dynamic architecture
            )
        ],
    )