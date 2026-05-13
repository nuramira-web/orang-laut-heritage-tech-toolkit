import json
import os
from pathlib import Path

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-word-input.json")
OUTPUT_PATH = Path("generated-vocabulary-entry.json")


def load_input(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Could not find input file: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_permissions(data: dict) -> None:
    permissions = data.get("permissions", {})
    sensitivity = data.get("sensitivity_level", "")

    allowed = (
        permissions.get("education_use") == "Yes"
        and permissions.get("ai_use") == "Yes"
    )

    restricted = sensitivity in [
        "Family restricted",
        "Culturally sensitive",
        "Spiritually sensitive"
    ]

    if not allowed:
        raise ValueError("This entry is not approved for educational and AI-assisted use.")

    if restricted:
        raise ValueError("This entry is sensitive or restricted and should not be processed by this tool.")


def generate_vocabulary_entry(data: dict) -> dict:
    prompt = f"""
You are the Disappearing Words AI Tool for the Pulau Brani Project.

Your task is to help create a careful draft vocabulary archive entry.

Rules:
- Use only the information provided.
- Do not invent origins, ritual meanings, histories, or community claims.
- Preserve uncertainty.
- Do not flatten dialect into standard language.
- Do not present one family or community usage as universal.
- Flag any areas that require community review.
- Suggest gentle follow-up questions for elders or community contributors.
- Include AI uncertainty notes.

Input:
{json.dumps(data, ensure_ascii=False, indent=2)}

Return JSON with:
- term
- language_or_dialect
- plain_meaning
- context_of_use
- cultural_or_emotional_meaning
- possible_related_themes
- related_archive_categories
- suggested_follow_up_questions
- sensitivity_notes
- uncertainty_notes
- draft_catalog_entry
- review_status
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "disappearing_words_entry",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "term": {"type": "string"},
                        "language_or_dialect": {"type": "string"},
                        "plain_meaning": {"type": "string"},
                        "context_of_use": {"type": "string"},
                        "cultural_or_emotional_meaning": {"type": "string"},
                        "possible_related_themes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "related_archive_categories": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "suggested_follow_up_questions": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "sensitivity_notes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "uncertainty_notes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "draft_catalog_entry": {"type": "string"},
                        "review_status": {
                            "type": "string",
                            "enum": ["needs_review"]
                        }
                    },
                    "required": [
                        "term",
                        "language_or_dialect",
                        "plain_meaning",
                        "context_of_use",
                        "cultural_or_emotional_meaning",
                        "possible_related_themes",
                        "related_archive_categories",
                        "suggested_follow_up_questions",
                        "sensitivity_notes",
                        "uncertainty_notes",
                        "draft_catalog_entry",
                        "review_status"
                    ]
                }
            }
        }
    )

    return json.loads(response.output_text)


def save_output(output: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(f"Saved generated vocabulary entry to {path}")


def main() -> None:
    data = load_input(INPUT_PATH)
    validate_permissions(data)
    output = generate_vocabulary_entry(data)
    save_output(output, OUTPUT_PATH)


if __name__ == "__main__":
    main()
