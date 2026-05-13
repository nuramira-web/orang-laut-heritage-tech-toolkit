import json
import os
from pathlib import Path

from openai import OpenAI

# ------------------------------------------------------------
# AI Remix Studio
# Pulau Brani Project / AI Heritage Lab
# ------------------------------------------------------------
#
# This tool helps students create AI-assisted heritage remix drafts
# while also producing a self-critical evaluation of the AI's role.
#
# It is designed for educational use.
# AI output should be reviewed before public use.
# ------------------------------------------------------------

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-remix-input.json")
OUTPUT_PATH = Path("ai-remix-output.json")


def load_remix_input(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Could not find input file: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_permissions(data: dict) -> None:
    permissions = data.get("source_material", {}).get("permissions", {})
    sensitivity = data.get("source_material", {}).get("sensitivity_level", "")

    allowed = (
        permissions.get("education_use") == "Yes"
        and permissions.get("creative_remix_use") == "Yes"
        and permissions.get("ai_use") == "Yes"
    )

    restricted = sensitivity in [
        "Family restricted",
        "Culturally sensitive",
        "Spiritually sensitive"
    ]

    if not allowed:
        raise ValueError("This material is not approved for educational, creative remix, and AI use.")

    if restricted:
        raise ValueError("This material is restricted or sensitive and should not be processed by this tool.")


def generate_remix(data: dict) -> dict:
    prompt = f"""
You are the AI Remix Studio for the Pulau Brani Project.

Your task is to help a student create a respectful, source-grounded heritage remix.

You must also evaluate your own role critically.

Rules:
- Use only the source material provided.
- Do not invent names, dates, places, rituals, family histories, or historical claims.
- Do not universalise one memory into a whole community story.
- Preserve cultural context and emotional nuance.
- Keep uncertainty visible.
- Avoid sensationalism, exoticism, trauma aesthetics, or vague mystical language.
- Treat AI as creative support, not cultural authority.
- Include a self-critical evaluation of what AI may have flattened, missed, or over-shaped.

Remix input:
{json.dumps(data, ensure_ascii=False, indent=2)}

Return JSON with:
- remix_title
- remix_format
- remix_draft
- source_grounding_notes
- cultural_context_notes
- ai_contribution
- human_revision_suggestions
- risks_and_sensitivities
- what_ai_may_have_flattened
- what_ai_may_have_amplified
- what_requires_review
- student_reflection_questions
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "ai_remix_studio_output",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "remix_title": {"type": "string"},
                        "remix_format": {"type": "string"},
                        "remix_draft": {"type": "string"},
                        "source_grounding_notes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "cultural_context_notes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "ai_contribution": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "human_revision_suggestions": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "risks_and_sensitivities": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "what_ai_may_have_flattened": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "what_ai_may_have_amplified": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "what_requires_review": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "student_reflection_questions": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": [
                        "remix_title",
                        "remix_format",
                        "remix_draft",
                        "source_grounding_notes",
                        "cultural_context_notes",
                        "ai_contribution",
                        "human_revision_suggestions",
                        "risks_and_sensitivities",
                        "what_ai_may_have_flattened",
                        "what_ai_may_have_amplified",
                        "what_requires_review",
                        "student_reflection_questions"
                    ]
                }
            }
        }
    )

    return json.loads(response.output_text)


def save_output(output: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(f"Saved remix output to {path}")


def main() -> None:
    data = load_remix_input(INPUT_PATH)
    validate_permissions(data)
    output = generate_remix(data)
    save_output(output, OUTPUT_PATH)


if __name__ == "__main__":
    main()
