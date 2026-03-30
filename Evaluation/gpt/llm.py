from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

try:
    llm = ChatOpenAI(
        model="gpt-4o",
        max_tokens=1024,
        timeout=None,
        max_retries=2,
    )
    print(f"Connected to Gemini API")
    print(f"Using model: {llm.model}")
except Exception as e:
    print(f"Error initializing Gemini: {e}")
    raise