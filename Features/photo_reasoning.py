from fastapi import APIRouter, File, UploadFile
import openai
import base64

router = APIRouter()

@router.post("/photo-reason")
async def photo_reasoning(image: UploadFile = File(...)):
    content = await image.read()
    encoded = base64.b64encode(content).decode()

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "Analyze the content of this image"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}
        ]}]
    )
    return {"analysis": response['choices'][0]['message']['content']}
