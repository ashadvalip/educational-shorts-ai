import sys
from src.planner.scene_planner import generate_script
from src.renderer.manim_renderer import render_video


def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "Backpropagation"
    script = generate_script(topic)

    print(script.model_dump_json(indent=2))
    render_video(script)


if __name__ == "__main__":
    main()