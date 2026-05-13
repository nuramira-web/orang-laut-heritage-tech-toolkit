import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-audience-input.json")
OUTPUT_PATH = Path("audience-translations.json")


def load_input(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def translate_for_audiences(data: dict) -> dict:
    prompt = f"""
You are the Audience Translator for the Pulau Brani Project.

Adapt the core message for each target audience.

Rules:
- Preserve meaning and nuance.
- Do not invent facts.
- Do not flatten Orang Laut, Orang Pulau, or island communities.
- Avoid sensationalism and romanticisation.
- Make the message legible for each audience.
- Include what to emphasise and what to avoid.

Input:
{json.dumps(data, ensure_ascii=False, indent=2)}

Return JSON with:
- audience_versions
- framing_notes
- risks_to_avoid
- review_notes
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {"raw_output": response.output_text}


def main():
    data = load_input(INPUT_PATH)
    output = translate_for_audiences(data)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
