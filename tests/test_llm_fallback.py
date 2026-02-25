import os
from src.planner.llm_planner import generate_script_with_llm


def test_llm_without_key():
    os.environ.pop("OPENAI_API_KEY", None)

    try:
        generate_script_with_llm("Test Topic")
    except EnvironmentError:
        assert True