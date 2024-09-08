from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import queue
import threading
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gelen istek verileri için Pydantic modeli
class ProductionRequest(BaseModel):
    prompts: list[str]  # prompt bir liste
    styles: list[str]  # style bir liste
    uid: str
    model: str
    quantity: int

def generate_image(requestBody):
    try:
        response = requests.post(
            "https://api.artaistapp.com/generate/v2",
            json={"prompt": requestBody.prompts[0], "style": requestBody.styles[0], "uid": requestBody.uid, "model": requestBody.model}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API hatası: {str(e)}")

# API İsteklerini kabul eden route
@app.post("/produce")
async def produce(request: ProductionRequest):
    print(request)

    result = []

    for _ in range(request.quantity):
        response = generate_image(request)
        result.append(response)

    print(len(result))
    print(result[-1])
    return result

# Uvicorn'u programatik olarak başlatma
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
