from fastapi import FastAPI, HTTPException, Form 
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch 
from PIL import Image
import io
import base64

app = FastAPI()

model_path = "/app/models/v1-5-pruned-emaonly.safetensors"
pipe = StableDiffusionPipeline.from_single_file(
    model_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

class SD_Request(BaseModel):
    prompt: str
    width: int = 512
    height: int = 512

@app.post("/generate")
def generate_image(request: SD_Request):
    try:
        if request.width < 128 or request.width > 1024 or request.height < 128 or request.height > 1024:
            raise HTTPException(status_code=400, detail="Width and height must be between 128 and 1024")
        width = (request.width // 8) * 8
        height = (request.height // 8) * 8
        image = pipe(prompt=request.prompt, width=width, height=height).images[0]
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return JSONResponse(content={"image_base64": img_str})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))