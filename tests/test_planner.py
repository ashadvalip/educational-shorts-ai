from src.planner.scene_planner import generate_script, VisualType


def test_script_generation():
    script = generate_script("Backpropagation")

    assert len(script.scenes) == 2
    assert script.scenes[0].visual == VisualType.NEURAL_NETWORK
    assert script.scenes[1].visual == VisualType.EQUATION
    assert script.scenes[1].equation_steps is not None