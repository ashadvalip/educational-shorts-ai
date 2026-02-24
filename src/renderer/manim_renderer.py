from manim import *
from src.planner.scene_planner import Script


class DynamicScene(Scene):
    def __init__(self, script: Script, **kwargs):
        self.script = script
        super().__init__(**kwargs)

    def construct(self):
        for scene in self.script.scenes:
            title = Text(scene.voiceover, font_size=36)
            self.play(Write(title))
            self.wait(scene.duration)
            self.play(FadeOut(title))


def render_video(script: Script):
    from manim import config

    config.media_dir = "media"
    config.output_file = "output_video"

    scene = DynamicScene(script)
    scene.render()