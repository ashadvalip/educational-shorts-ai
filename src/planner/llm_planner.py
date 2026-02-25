import os
import json
import re
import time
from typing import Any
from openai import OpenAI
from pydantic import ValidationError

from src.planner.scene_planner import Script


MAX_RETRIES = 2


def generate_script_with_llm(topic: str) -> Script:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=api_key)

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": _build_prompt(topic)}],
                temperature=0.3,
            )

            raw_content = response.choices[0].message.content

            cleaned_json = _extract_json(raw_content)

            data: Any = json.loads(cleaned_json)

            script = Script.model_validate(data)

            return script

        except (json.JSONDecodeError, ValidationError) as e:
            print(f"[LLM WARNING] Invalid JSON/Schema (attempt {attempt+1}): {e}")

            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue
            else:
                raise ValueError("LLM failed to produce valid structured output.")

        except Exception as e:
            raise RuntimeError(f"Unexpected LLM failure: {e}")

    raise RuntimeError("LLM generation failed after retries.")


# ------------------------------
# Prompt Builder
# ------------------------------
def _build_prompt(topic: str) -> str:
    return f"""
You are an educational AI system.

Generate a structured JSON explanation for:
"{topic}"

IMPORTANT:
- Return ONLY raw JSON.
- No markdown.
- No explanations.
- No triple backticks.

Schema:

{{
  "title": string,
  "scenes": [
    {{
      "voiceover": string,
      "visual": "neural_network" | "equation" | "text",
      "duration": float,
      "layers": [int] (optional),
      "equation_steps": [string] (optional)
    }}
  ]
}}

Constraints:
- 2–3 scenes maximum
- Keep durations realistic (3–8 seconds)
- Only include required fields
"""


# ------------------------------
# JSON Extraction
# ------------------------------
def _extract_json(content: str) -> str:
    """
    Removes markdown formatting if present.
    Extracts first JSON object found.
    """

    # Remove markdown code fences
    content = re.sub(r"```json", "", content)
    content = re.sub(r"```", "", content)

    # Extract JSON object
    match = re.search(r"\{.*\}", content, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in LLM output.")

    return match.group(0)