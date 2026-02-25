from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class VisualType(str, Enum):
    TEXT = "text"
    NEURAL_NETWORK = "neural_network"
    EQUATION = "equation"


class Scene(BaseModel):
    voiceover: str
    visual: VisualType
    duration: float
    layers: Optional[List[int]] = None
    equation_steps: Optional[List[str]] = None


class Script(BaseModel):
    title: str
    scenes: List[Scene]


def generate_script(topic: str) -> Script:
    """
    Deterministic multi-scene script.
    Includes neural network + animated equation transformation.
    """

    return Script(
        title=f"{topic} Explained",
        scenes=[
            Scene(
                voiceover=f"{topic} uses a neural network structure.",
                visual=VisualType.NEURAL_NETWORK,
                duration=4.0,
                layers=[3, 4, 2],
            ),
            Scene(
                voiceover="The loss function measures prediction error.",
                visual=VisualType.EQUATION,
                duration=6.0,
                equation_steps=[
                    r"L = \frac{1}{2}(y - \hat{y})^2",
                    r"\frac{\partial L}{\partial \hat{y}} = (\hat{y} - y)",
                    r"\frac{\partial L}{\partial w} = (\hat{y} - y)x",
                ],
            ),
        ],
    )