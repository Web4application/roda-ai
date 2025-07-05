from fastapi import APIRouter
from pydantic import BaseModel
import openai

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_bot(data: Message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": data.message}]
    )
    return {"reply": response['choices'][0]['message']['content']}
