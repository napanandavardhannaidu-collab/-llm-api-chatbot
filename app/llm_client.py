
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"

SYSTEM_PROMPT = """
You are DevBot, a friendly AI assistant specializing in
DevOps, Cloud Computing, Linux, Docker, Kubernetes and CI/CD.

Explain concepts clearly, provide practical examples,
help troubleshoot problems, and maintain conversation context.
"""

def generate_response(history, user_message):

    contents = []

    for message in history:
        role = "model" if message["role"] == "assistant" else "user"

        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=message["content"])]
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7
        )
    )

    return response.text
