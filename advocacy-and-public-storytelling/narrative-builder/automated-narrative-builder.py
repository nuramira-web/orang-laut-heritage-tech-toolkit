import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

OUTPUT_PATH = Path("generated-narrative.json")


def ask_user_questions():
    print("\nPulau Brani Narrative Builder\n")

    return {
        "topic": input("What is the topic or issue? "),
        "core_issue": input("What is the core issue or opportunity? "),
        "intended_audience": input("Who is the audience? "),
        "goal": input("What do you want the audience to understand or do? "),
        "source_materials": input("What evidence or materials are you using? "),
        "emotional_themes": input("What emotions are present? "),
        "tone": input("What tone should this have? "),
        "constraints": input("What should the AI avoid? ")
    }


def generate_narrative(data):
    prompt = f"""
You are the Narrative Builder for the Pulau Brani Project.

Create a thoughtful, ethical, source-grounded public narrative.

Rules:
- Use only the information provided.
- Do not invent facts.
- Preserve nuance.
- Avoid sensationalism.
- Avoid romanticising displacement.
- Avoid flattening Orang Laut, Orang Pulau, or island communities.
- Balance emotion with evidence.
- Include review notes.

Input:
{json.dumps(data, ensure_ascii=False, indent=2)}

Generate:
1. Title
2. One-sentence key message
3. Short public narrative
4. Presentation outline
5. Audience framing
6. Suggested call to action
7. Risks or sensitivities
8. What needs human/community review
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


def main():
    data = ask_user_questions()
    narrative = generate_narrative(data)

    result = {
        "input": data,
        "generated_narrative": narrative
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    print("\nNarrative generated successfully.")
    print(f"Saved to: {OUTPUT_PATH}\n")
    print(narrative)


if __name__ == "__main__":
    main()
