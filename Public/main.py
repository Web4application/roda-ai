# roda_ai.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

class AIResponse(BaseModel):
    response: str

def run_roda_ai(prompt: str) -> str:
    # Stub your AI logic here, e.g., call your model
    # For now, just echo input reversed as dummy response
    return prompt[::-1]

@app.post("/api/generate", response_model=AIResponse)
async def generate_text(prompt: Prompt):
    result = run_roda_ai(prompt.prompt)
    return AIResponse(response=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
