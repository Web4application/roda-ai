from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend on Vercel to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or whitelist your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    # 👇 Here you can call OpenAI or custom logic
    if "deploy" in prompt.lower():
        reply = "Sure! I can help you deploy your Web4 project."
    else:
        reply = f"I received: {prompt}"

    return { "reply": reply }
