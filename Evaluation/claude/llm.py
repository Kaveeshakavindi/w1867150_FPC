# llm.py
from dotenv import load_dotenv
import os
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=api_key,
    temperature=0,
    max_tokens=1024,
    timeout=None,
)
