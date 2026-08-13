import os
from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """You are a prompt transformation compiler. Output ONLY the raw prompt text starting directly with the title block. Do NOT include introductory messages, conversational text (e.g. 'To create a high-quality...'), meta-explanations, or markdown wrappers like ```markdown unless asked. Your output must be copy-paste ready for an AI agent."""

def get_structured_prompt(informal_prompt: str) -> str:
    # Initialize client (picks up GEMINI_API_KEY or GOOGLE_API_KEY)
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=informal_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0,
        ),
    )
    if not response.text:
        raise RuntimeError("The model returned an empty response.")
    return response.text
