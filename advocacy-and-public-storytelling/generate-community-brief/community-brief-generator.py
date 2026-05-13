import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INPUT_PATH = Path("sample-brief-input.json")
OUTPUT_PATH = Path("generated-community-brief.json")


def load_input(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_brief(data):
    prompt = f"""
You are the Community Brief Generator for the Pulau Brani Project.

Generate a short, accessible, ethical community brief.

Rules:
- Preserve nuance.
- Avoid sensationalism.
- Avoid flattening communities.
- Preserve uncertainty where appropriate.
- Explain public relevance clearly.
- Keep language accessible.

Input:
{json.dumps(data, ensure_ascii=False, indent=2)}

Generate:
- title
- summary
- key findings
- public relevance
- suggested next steps
- questions for reflection
- risks to avoid
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {"raw_output": response.output_text}


def main():
    data = load_input(INPUT_PATH)
    output = generate_brief(data)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
