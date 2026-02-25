from manim import *
from typing import List
from src.planner.scene_planner import Script, VisualType


class DynamicScene(Scene):
    def __init__(self, script: Script, **kwargs):
        self.script = script
        super().__init__(**kwargs)

    def construct(self):
        for scene in self.script.scenes:
            if scene.visual == VisualType.TEXT:
                self.render_text(scene.voiceover, scene.duration)

            elif scene.visual == VisualType.NEURAL_NETWORK:
                self.render_neural_network(scene.layers, scene.duration)

    def render_text(self, text_content: str, duration: float):
        text = Text(text_content, font_size=36)
        self.play(Write(text))
        self.wait(duration)
        self.play(FadeOut(text))

    def render_neural_network(self, layers: List[int], duration: float):
        network = VGroup()

        layer_spacing = 2.5
        neuron_spacing = 0.8

        neurons = []
        edges = VGroup()

        for i, layer_size in enumerate(layers):
            layer_group = VGroup()
            for j in range(layer_size):
                neuron = Circle(radius=0.2, color=BLUE)
                neuron.move_to(
                    RIGHT * i * layer_spacing + UP * (j - layer_size / 2) * neuron_spacing
                )
                layer_group.add(neuron)
            neurons.append(layer_group)
            network.add(layer_group)

        # Connect layers
        for i in range(len(neurons) - 1):
            for neuron1 in neurons[i]:
                for neuron2 in neurons[i + 1]:
                    line = Line(
                        neuron1.get_right(),
                        neuron2.get_left(),
                        stroke_width=1,
                        color=GRAY,
                    )
                    edges.add(line)

        self.play(Create(network))
        self.play(Create(edges))
        self.wait(duration)
        self.play(FadeOut(network), FadeOut(edges))


def render_video(script: Script):
    from manim import config

    config.media_dir = "media"
    config.output_file = "output_video"

    scene = DynamicScene(script)
    scene.render()