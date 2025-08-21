from fastapi import FastAPI
from pydantic import BaseModel
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load PEGASUS model
model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

class TextRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize_text(req: TextRequest):
    inputs = tokenizer(req.text, truncation=True, padding="longest", return_tensors="pt")
    summary_ids = model.generate(**inputs, max_length=60, min_length=20, length_penalty=2.0, num_beams=4)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)