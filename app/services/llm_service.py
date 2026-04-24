import google.generativeai as genai
from app.config import Config

# Configure Gemini AI
genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_from_gemini(prompt: str):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        if response and response.text:
            return {"response": response.text}
        else:
            raise Exception("Empty response from Gemini")

    except Exception as e:
        raise Exception(f"Gemini API request failed: {str(e)}")