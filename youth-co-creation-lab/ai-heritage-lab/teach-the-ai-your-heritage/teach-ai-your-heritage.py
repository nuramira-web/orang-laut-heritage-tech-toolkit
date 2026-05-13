import json
import os
from pathlib import Path

from openai import OpenAI

# ------------------------------------------------------------
# Teach the AI Your Heritage
# Pulau Brani Project / AI Heritage Lab
# ------------------------------------------------------------
#
# This tool lets students test how an AI system interprets
# cultural knowledge.
#
# It produces:
# 1. An AI explanation
# 2. A nuance analysis
# 3. A hallucination / uncertainty check
# 4. Suggested corrections
# 5. Reflection questions
#
# AI output is for learning and review only.
# It should not be treated as final heritage interpretation.
# ------------------------------------------------------------

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-teaching-session.json")
OUTPUT_PATH = Path("ai-teaching-output.json")


def load_teaching_session(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path}. Create a teaching session JSON file first."
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def analyse_heritage_item(session: dict) -> dict:
    prompt = f"""
You are part of the Pulau Brani Project's AI Heritage Lab.

A student is testing how AI interprets cultural heritage knowledge.

Your job is to respond carefully and then analyse your own response.

Rules:
- Use only the information provided by the student.
- Do not invent historical claims, origins, dates, names, places, or rituals.
- Preserve uncertainty.
- Do not universalise one family or community memory.
- Respect cultural nuance.
- Flag sensitive areas.
- Explain what requires human or community review.

Student teaching session:
{json.dumps(session, ensure_ascii=False, indent=2)}

Return JSON with:
1. ai_explanation
2. what_the_ai_understood
3. what_may_be_missing
4. possible_flattening_or_oversimplification
5. hallucination_risks
6. sensitivity_notes
7. suggested_corrections
8. improved_prompt_for_next_attempt
9. student_reflection_questions
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "teach_ai_your_heritage_output",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "ai_explanation": {"type": "string"},
                        "what_the_ai_understood": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "what_may_be_missing": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "possible_flattening_or_oversimplification": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "hallucination_risks": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "sensitivity_notes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "suggested_corrections": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "improved_prompt_for_next_attempt": {"type": "string"},
                        "student_reflection_questions": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": [
                        "ai_explanation",
                        "what_the_ai_understood",
                        "what_may_be_missing",
                        "possible_flattening_or_oversimplification",
                        "hallucination_risks",
                        "sensitivity_notes",
                        "suggested_corrections",
                        "improved_prompt_for_next_attempt",
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

    print(f"Saved AI teaching output to {path}")


def main() -> None:
    session = load_teaching_session(INPUT_PATH)
    output = analyse_heritage_item(session)
    save_output(output, OUTPUT_PATH)


if __name__ == "__main__":
    main()
