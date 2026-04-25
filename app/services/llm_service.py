import os
from google import genai

def generate_from_llm(prompt: str):
    try:
        client = genai.Client()  # otomatis baca GEMINI_API_KEY dari .env

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        raw_text = response.text

        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1)
            raw_text = raw_text.replace("```", "")
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "")

        raw_text = raw_text.strip()

        return {"response": raw_text}

    except Exception as e:
        raise Exception(f"PESAN ASLI GEMINI: {str(e)}")