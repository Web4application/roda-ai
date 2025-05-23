from fastapi import APIRouter, Request
from pydantic import BaseModel
import openai

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/summarize")
async def summarize_text(data: TextInput):
    prompt = f"Summarize the following: {data.text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response['choices'][0]['message']['content']
    return {"summary": summary.strip()}
