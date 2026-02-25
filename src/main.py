import sys
import os
from dotenv import load_dotenv

from src.planner.scene_planner import generate_script
from src.planner.llm_planner import generate_script_with_llm
from src.renderer.manim_renderer import render_video


def main():
    # Load environment variables (development only)
    load_dotenv()

    topic = sys.argv[1] if len(sys.argv) > 1 else "Backpropagation"

    use_llm = os.getenv("USE_LLM", "false").lower() == "true"

    if use_llm:
        script = _generate_with_llm_safe(topic)
    else:
        script = generate_script(topic)

    print(script.model_dump_json(indent=2))
    render_video(script)


def _generate_with_llm_safe(topic: str):
    try:
        return generate_script_with_llm(topic)
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        print("[INFO] Falling back to deterministic planner.")
        return generate_script(topic)


if __name__ == "__main__":
    main()