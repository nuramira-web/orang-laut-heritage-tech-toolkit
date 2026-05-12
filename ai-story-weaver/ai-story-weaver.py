import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SOURCE_TEXT = """
Paste approved oral history excerpt, recipe note, object description, or memory fragment here.
"""

PROMPT = f"""
You are the AI Story Weaver for the Pulau Brani Project.

Use only the source material below. Do not invent details.

Source material:
{SOURCE_TEXT}

Create:
1. Title
2. Short summary
3. Respectful heritage story draft
4. Key themes
5. Emotional tones
6. Suggested follow-up questions
7. Sensitivity notes
8. Suggested archive tags
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=PROMPT
)

print(response.output_text)
