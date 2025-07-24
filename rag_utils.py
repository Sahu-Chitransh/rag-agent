import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import docx
import os
import requests
import json
from config import OPENROUTER_API_KEY, LLM_API_URL, LLM_MODEL


def process_document(path):
    ext = os.path.splitext(path)[1].lower()
    text = ""

    if ext == ".pdf":
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
        doc.close()

    elif ext == ".docx":
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif ext in [".png", ".jpg", ".jpeg"]:
        image = Image.open(path)
        text = pytesseract.image_to_string(image)

    else:
        raise ValueError("Unsupported file format")

    return text


def query_llm(context, question):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the given document."},
            {"role": "user", "content": f"Document:\n{context}\n\nQuestion:\n{question}"}
        ]
    }

    response = requests.post(LLM_API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def transcribe_audio(audio_path):
    with open(audio_path, "rb") as f:
        audio_data = f.read()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Assume OpenRouter routes to Whisper-like API. Modify if using another transcription API
    response = requests.post(
        "https://openrouter.ai/api/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        files={"file": ("audio.wav", audio_data, "audio/wav")}
    )

    if response.status_code != 200:
        raise Exception(f"Transcription failed: {response.text}")

    return response.json().get("text", "")
