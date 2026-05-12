import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INTERVIEW_EXCERPT = """
Paste interview excerpt here.
"""

PROMPT = f"""
You are the Oral History Companion for the Pulau Brani Project.

Based only on this interview excerpt:

{INTERVIEW_EXCERPT}

Suggest:
1. Gentle follow-up questions
2. Themes
3. Metadata tags
4. Sensitive areas to handle carefully
5. Possible links to archive categories
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=PROMPT
)

print(response.output_text)
