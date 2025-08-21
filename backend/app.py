from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

origins = [
    "http://localhost:5173",  # your Vite frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # allow POST, OPTIONS, etc.
    allow_headers=["*"],
)

HF_API_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    raise ValueError("Set HF_API_TOKEN in your environment")
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

class TextRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(request: TextRequest):
    payload = {"inputs": request.text}
    response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
    data = response.json()
    # Hugging Face returns a list of dicts with 'summary_text'
    if isinstance(data, list) and "summary_text" in data[0]:
        return {"summary": data[0]["summary_text"]}
    else:
        return {"error": data}

