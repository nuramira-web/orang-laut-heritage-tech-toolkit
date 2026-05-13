import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-presentation-input.json")
OUTPUT_PATH = Path("generated-presentation.json")


def load_input(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_presentation(data):
    prompt = f"""
You are the Presentation Builder for the Pulau Brani Project.

Generate a thoughtful, ethical presentation structure.

Rules:
- Preserve nuance.
- Avoid sensationalism.
- Balance emotion and evidence.
- Make the presentation engaging but not manipulative.
- Include audience participation moments where appropriate.

Input:
{json.dumps(data, ensure_ascii=False, indent=2)}

Generate:
- title
- presentation arc
- slide outline
- emotional flow
- audience engagement moments
- key messages
- speaking notes
- risks to avoid
- reflection questions
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {"raw_output": response.output_text}


def main():
    data = load_input(INPUT_PATH)
    output = generate_presentation(data)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
