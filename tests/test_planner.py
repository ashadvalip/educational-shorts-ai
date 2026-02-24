from src.planner.scene_planner import generate_script


def test_script_generation():
    script = generate_script("Backpropagation")
    assert script.title == "Backpropagation Explained"
    assert len(script.scenes) > 0
    