import json
import os
from pathlib import Path
from openai import OpenAI

# --------------------------------------------
# Pulau Brani Memory Constellation Engine
# AI Connection Suggester
# --------------------------------------------
# Purpose:
# Reads approved archive items and suggests relationships between them.
#
# Important:
# - Only use items approved for public / educational / AI use.
# - AI suggestions are drafts.
# - Human/community review is still required.
# --------------------------------------------

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ARCHIVE_PATH = Path("../community-archive/archive-items.json")
OUTPUT_PATH = Path("ai-generated-memory-graph.json")


def load_archive_items():
    with ARCHIVE_PATH.open("r", encoding="utf-8") as file:
        items = json.load(file)

    approved_items = []

    for item in items:
        public_ok = item.get("public_use") in ["Yes", "Limited"]
        education_ok = item.get("education_use") == "Yes"
        ai_ok = item.get("ai_use") == "Yes"
        restricted = item.get("sensitivity_level") in [
            "Family restricted",
            "Culturally sensitive",
            "Spiritually sensitive"
        ]

        if public_ok and education_ok and ai_ok and not restricted:
            approved_items.append(item)

    return approved_items


def suggest_connections(items):
    prompt = f"""
You are helping build the Pulau Brani Memory Constellation Engine.

Your task is to suggest careful, source-grounded relationships between approved archive items.

Rules:
- Do not invent facts.
- Only use the archive items provided.
- Do not reveal restricted or private knowledge.
- Mark all AI-generated relationships as "needs_review".
- Use culturally respectful language.
- Preserve nuance around Orang Laut, Orang Pulau, and Pulau Brani communities.
- If a connection is uncertain, describe it as interpretive.

Archive items:
{json.dumps(items, ensure_ascii=False, indent=2)}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "memory_constellation_graph",
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
                                    "type": {"type": "string"},
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "themes": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "emotions": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "source_id": {"type": "string"},
                                    "public_use": {"type": "string"}
                                },
                                "required": [
                                    "id",
                                    "type",
                                    "title",
                                    "description",
                                    "themes",
                                    "emotions",
                                    "source_id",
                                    "public_use"
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
                        }
                    },
                    "required": ["nodes", "links"]
                }
            }
        }
    )

    return json.loads(response.output_text)


def save_graph(graph):
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(graph, file, ensure_ascii=False, indent=2)

    print(f"Saved AI-generated graph to {OUTPUT_PATH}")


if __name__ == "__main__":
    archive_items = load_archive_items()

    if not archive_items:
        raise ValueError("No approved archive items found for AI-assisted connection generation.")

    graph = suggest_connections(archive_items)
    save_graph(graph)
