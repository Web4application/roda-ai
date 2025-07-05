from fastapi import APIRouter
from pydantic import BaseModel
import openai

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/function-call")
async def function_call(query: Query):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query.query}],
        functions=[
            {
                "name": "get_time",
                "description": "Returns the current time",
                "parameters": {}
            }
        ]
    )
    return {"result": response['choices'][0]['message']['content']}
