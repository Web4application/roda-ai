from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client with API key
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LeadRequest(BaseModel):
    name: str
    email: str
    message: str

@app.post("/auto_reply")
async def auto_reply(lead: LeadRequest):
    prompt = f"""You're RODA AI, a smart assistant. A user named {lead.name} just submitted:
Email: {lead.email}
Message: {lead.message}
Write a helpful, friendly reply to thank them and offer next steps."""
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    reply = response.choices[0].message.content
    return { "reply": reply }