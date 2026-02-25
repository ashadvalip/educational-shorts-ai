from src.planner.scene_planner import generate_script, VisualType


def test_script_generation():
    script = generate_script("Backpropagation")

    assert script.title == "Backpropagation Explained"
    assert len(script.scenes) == 1
    assert script.scenes[0].visual == VisualType.NEURAL_NETWORK
    assert script.scenes[0].layers == [3, 4, 2]