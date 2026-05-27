import os

try:
	from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency fallback
	load_dotenv = None


if load_dotenv is not None:
	load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")