import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-memory-input.json")
OUTPUT_PATH = Path("generated-memory-constellation.json")


def load_source_materials(path: Path):
    with path.open("r", encoding="utf-8") as file:
        materials = json.load(file)

    approved = []

    for item in materials:
        public_ok = item.get("public_use") in ["Yes", "Limited"]
        education_ok = item.get("education_use") == "Yes"
        ai_ok = item.get("ai_use") == "Yes"
        restricted = item.get("sensitivity_level") in [
            "Family restricted",
            "Culturally sensitive",
            "Spiritually sensitive"
        ]

        if public_ok and education_ok and ai_ok and not restricted:
            approved.append(item)

    return approved


def build_constellation(materials):
    prompt = f"""
You are the Memory Constellation Builder for the Pulau Brani Project.

Identify careful, source-grounded relationships between the approved heritage materials below.

Rules:
- Use only provided materials.
- Do not invent names, dates, rituals, family histories, or places.
- Do not reveal restricted or private knowledge.
- Preserve nuance around Orang Laut, Orang Pulau, Pulau Brani, and island communities.
- Mark all AI-generated nodes and links as needs_review.
- If a relationship is uncertain, say so in the reason.
- Emotional tags must be supported by the material.

Approved materials:
{json.dumps(materials, ensure_ascii=False, indent=2)}

Return valid JSON with:
- nodes
- links
- review_notes
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "memory_constellation",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "nodes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "id": {"type": "string"},
                                    "source_id": {"type": "string"},
                                    "title": {"type": "string"},
                                    "type": {"type": "string"},
                                    "description": {"type": "string"},
                                    "themes": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "emotions": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "review_status": {
                                        "type": "string",
                                        "enum": ["needs_review"]
                                    }
                                },
                                "required": [
                                    "id",
                                    "source_id",
                                    "title",
                                    "type",
                                    "description",
                                    "themes",
                                    "emotions",
                                    "review_status"
                                ]
                            }
                        },
                        "links": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "source": {"type": "string"},
                                    "target": {"type": "string"},
                                    "relationship": {"type": "string"},
                                    "reason": {"type": "string"},
                                    "confidence": {
                                        "type": "string",
                                        "enum": ["low", "medium", "high"]
                                    },
                                    "review_status": {
                                        "type": "string",
                                        "enum": ["needs_review"]
                                    }
                                },
                                "required": [
                                    "source",
                                    "target",
                                    "relationship",
                                    "reason",
                                    "confidence",
                                    "review_status"
                                ]
                            }
                        },
                        "review_notes": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["nodes", "links", "review_notes"]
                }
            }
        }
    )

    return json.loads(response.output_text)


def save_constellation(data, path: Path):
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Saved constellation to {path}")


if __name__ == "__main__":
    source_materials = load_source_materials(INPUT_PATH)

    if not source_materials:
        raise ValueError("No approved source materials available for AI processing.")

    constellation = build_constellation(source_materials)
    save_constellation(constellation, OUTPUT_PATH)
