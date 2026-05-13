import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-check-input.json")
OUTPUT_PATH = Path("ethical-persuasion-report.json")


def load_input(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def check_persuasion(data: dict) -> dict:
    prompt = f"""
You are the Ethical Persuasion Checker for the Pulau Brani Project.

Review the text for ethical storytelling and advocacy risks.

Check for:
- sensationalism
- overstatement
- romanticisation
- trauma aesthetics
- saviour framing
- cultural flattening
- unsupported claims
- vague urgency
- extractive storytelling
- weak community agency

Rules:
- Do not rewrite by making the message bland.
- Preserve urgency where justified.
- Preserve dignity, nuance, and clarity.
- Suggest stronger ethical alternatives.

Input:
{json.dumps(data, ensure_ascii=False, indent=2)}

Return JSON with:
- overall_assessment
- ethical_risks
- cultural_flattening_risks
- unsupported_or_overstated_claims
- language_to_reconsider
- stronger_rewrite
- explanation_of_rewrite
- review_recommendation
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {"raw_output": response.output_text}


def main():
    data = load_input(INPUT_PATH)
    output = check_persuasion(data)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
