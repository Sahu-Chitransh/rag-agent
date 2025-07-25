import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (add more as needed)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or ""

# Allowed upload file extensions
ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'png', 'jpg', 'jpeg',    # Document/image types
    'wav', 'mp3', 'm4a'                     # Audio types
}

# Uploads directory
UPLOAD_FOLDER = 'uploads'

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Whisper (audio transcription) endpoint (OpenRouter proxy to Whisper-1 / other)
WHISPER_API_URL = "https://openrouter.ai/api/v1/audio/transcriptions"

# LLM (chat/completion) API endpoint and model
LLM_API_URL = "https://openrouter.ai/api/v1/chat/completions"
LLM_MODEL = "mistralai/mistral-7b-instruct"    # or "openai/gpt-4", "anthropic/claude-3-haiku", etc.

# (Optional) maximum file size in bytes (e.g., 20MB)
MAX_CONTENT_LENGTH = 20 * 1024 * 1024   # 20 MB

# Flask secret key (for session security: set something strong in .env for production)
SECRET_KEY = os.getenv("FLASK_SECRET_KEY") or "rag_secret"
