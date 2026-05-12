import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

TEXT = """
Paste approved oral history excerpt here.
"""

PROMPT = f"""
You are helping with Heritage Emotion Mapping for the Pulau Brani Project.

Analyse the excerpt below and suggest emotional themes.

Rules:
- Use only evidence from the text.
- Do not impose emotions without support.
- Quote or paraphrase the evidence briefly.
- Mark uncertain emotional readings as tentative.
- Flag sensitive content.

Text:
{TEXT}

Return JSON with:
- emotional_themes
- evidence
- confidence
- sensitivity_notes
- suggested_tags
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=PROMPT
)

print(response.output_text)
