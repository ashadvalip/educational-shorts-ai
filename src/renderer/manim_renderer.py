from manim import *
from typing import List
from src.planner.scene_planner import Script, VisualType


class DynamicScene(Scene):
    def __init__(self, script: Script, **kwargs):
        self.script = script
        super().__init__(**kwargs)

    def construct(self):
        # -----------------------------
        # TITLE INTRO
        # -----------------------------
        self.render_title(self.script.title)

        for scene in self.script.scenes:

            if scene.visual == VisualType.NEURAL_NETWORK:
                self.render_neural_network(scene.layers, scene.duration)

            elif scene.visual == VisualType.EQUATION:
                self.render_equation(scene.equation_steps, scene.duration)

            elif scene.visual == VisualType.TEXT:
                self.render_text(scene.voiceover, scene.duration)

    # -----------------------------
    # TITLE
    # -----------------------------
    def render_title(self, title: str):
        title_text = Text(title, font_size=48)
        self.play(FadeIn(title_text))
        self.wait(1.5)
        self.play(FadeOut(title_text))

    # -----------------------------
    # TEXT
    # -----------------------------
    def render_text(self, text_content: str, duration: float):
        text = Text(text_content, font_size=36)
        self.play(Write(text))
        self.wait(duration)
        self.play(FadeOut(text))

    # -----------------------------
    # NEURAL NETWORK
    # -----------------------------
    def render_neural_network(self, layers: List[int], duration: float):
        network = VGroup()
        edges = VGroup()

        layer_spacing = 2.5
        neuron_spacing = 0.8

        neurons = []

        for i, layer_size in enumerate(layers):
            layer_group = VGroup()

            for j in range(layer_size):
                neuron = Circle(radius=0.2, color=BLUE)
                neuron.move_to(
                    RIGHT * i * layer_spacing
                    + UP * (j - layer_size / 2) * neuron_spacing
                )
                layer_group.add(neuron)

            neurons.append(layer_group)
            network.add(layer_group)

        # Create edges
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

        # Animate layer-by-layer
        for layer in neurons:
            self.play(Create(layer), run_time=0.6)

        self.play(Create(edges), run_time=1.0)

        self.wait(duration)
        self.play(FadeOut(network), FadeOut(edges))

    # -----------------------------
    # EQUATION (SMART TIMING)
    # -----------------------------
    def render_equation(self, steps: List[str], total_duration: float):

        math_objects = [MathTex(step) for step in steps]

        # Distribute duration evenly across steps
        per_step_time = total_duration / max(len(steps), 1)

        self.play(Write(math_objects[0]))
        self.wait(per_step_time / 2)

        for i in range(1, len(math_objects)):
            self.play(Transform(math_objects[0], math_objects[i]))
            self.wait(per_step_time / 2)

        self.play(FadeOut(math_objects[0]))


def render_video(script: Script):
    from manim import config
    import re

    # Clean filename from title
    safe_title = re.sub(r"[^\w\s-]", "", script.title).strip().lower()
    safe_title = re.sub(r"[-\s]+", "_", safe_title)

    config.media_dir = "media"
    config.output_file = safe_title

    scene = DynamicScene(script)
    scene.render()