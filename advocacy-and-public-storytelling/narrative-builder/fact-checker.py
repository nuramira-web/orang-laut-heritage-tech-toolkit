import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

NARRATIVE_PATH = Path("generated-narrative.json")
SOURCE_PATH = Path("sample-narrative-input.json")
OUTPUT_PATH = Path("fact-check-report.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Could not find {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def fact_check(narrative: dict, source: dict) -> dict:
    prompt = f"""
You are the Fact-Checker for the Pulau Brani Project Narrative Builder.

Your task is to compare a generated narrative against the source material provided.

Rules:
- Do not verify against outside knowledge.
- Only check whether claims are supported by the provided source material.
- Flag invented facts, unsupported claims, overstatements, vague claims, and risky generalisations.
- Pay special attention to Orang Laut, Orang Pulau, Pulau Brani, maritime heritage, rituals, foodways, and community memory.
- Preserve nuance and uncertainty.
- Recommend safer wording where needed.
- Flag anything requiring community or human review.

Source material:
{json.dumps(source, ensure_ascii=False, indent=2)}

Generated narrative:
{json.dumps(narrative, ensure_ascii=False, indent=2)}

Return JSON with:
- overall_assessment
- supported_claims
- unsupported_or_overstated_claims
- invented_or_unverified_details
- risky_generalisation
- community_review_needed
- safer_rewording_suggestions
- final_recommendation
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "fact_check_report",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "overall_assessment": {"type": "string"},
                        "supported_claims": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "unsupported_or_overstated_claims": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "invented_or_unverified_details": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "risky_generalisation": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "community_review_needed": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "safer_rewording_suggestions": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "final_recommendation": {"type": "string"}
                    },
                    "required": [
                        "overall_assessment",
                        "supported_claims",
                        "unsupported_or_overstated_claims",
                        "invented_or_unverified_details",
                        "risky_generalisation",
                        "community_review_needed",
                        "safer_rewording_suggestions",
                        "final_recommendation"
                    ]
                }
            }
        }
    )

    return json.loads(response.output_text)


def main() -> None:
    narrative = load_json(NARRATIVE_PATH)
    source = load_json(SOURCE_PATH)

    report = fact_check(narrative, source)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)

    print(f"Saved fact-check report to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
