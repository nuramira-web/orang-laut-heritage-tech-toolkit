import json
import os
from pathlib import Path

from openai import OpenAI

# ------------------------------------------------------------
# Narrative Builder
# Pulau Brani Project / Advocacy & Public Storytelling
# ------------------------------------------------------------
#
# This tool helps generate public storytelling narratives
# grounded in heritage, memory, evidence, and ethical framing.
#
# AI output requires human and community review.
# ------------------------------------------------------------

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-narrative-input.json")
OUTPUT_PATH = Path("generated-narrative.json")


def load_input(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Could not find input file: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def generate_narrative(data: dict) -> dict:
    prompt = f"""
You are the Narrative Builder for the Pulau Brani Project.

Your task is to help generate a thoughtful, ethical public narrative.

Rules:
- Use only the information provided.
- Do not invent facts or historical claims.
- Preserve nuance and uncertainty.
- Avoid flattening communities.
- Avoid trauma spectacle and romanticisation.
- Preserve contributor dignity.
- Balance emotion with evidence.
- Explain public relevance clearly.

Narrative input:
{json.dumps(data, ensure_ascii=False, indent=2)}

Return JSON with:
- title
- key_message
- narrative_arc
- emotional_framing
- evidence_used
- public_relevance
- suggested_call_to_action
- audience_notes
- possible_risks_or_flattening
- what_requires_review
- reflection_questions
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "narrative_builder_output",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "title": {"type": "string"},
                        "key_message": {"type": "string"},
                        "narrative_arc": {"type": "string"},
                        "emotional_framing": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "evidence_used": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "public_relevance": {"type": "string"},
                        "suggested_call_to_action": {"type": "string"},
                        "audience_notes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "possible_risks_or_flattening": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "what_requires_review": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "reflection_questions": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": [
                        "title",
                        "key_message",
                        "narrative_arc",
                        "emotional_framing",
                        "evidence_used",
                        "public_relevance",
                        "suggested_call_to_action",
                        "audience_notes",
                        "possible_risks_or_flattening",
                        "what_requires_review",
                        "reflection_questions"
                    ]
                }
            }
        }
    )

    return json.loads(response.output_text)


def save_output(output: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(f"Saved generated narrative to {path}")


def main() -> None:
    data = load_input(INPUT_PATH)
    output = generate_narrative(data)
    save_output(output, OUTPUT_PATH)


if __name__ == "__main__":
    main()
