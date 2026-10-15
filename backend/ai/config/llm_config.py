import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Models
FAST_MODEL   = "openai/gpt-oss-20b"   # outline, planning
WRITER_MODEL = "openai/gpt-oss-20b"   # blog writing


def get_llm(temperature=0.7, fast=False):
    key = os.getenv("GROQ_API_KEY")

    if not key:
        raise ValueError("GROQ_API_KEY missing from .env")

    return ChatGroq(
        model=FAST_MODEL if fast else WRITER_MODEL,
        temperature=temperature,
        groq_api_key=key,
        max_tokens=1200   # ✅ prevent errors
    )