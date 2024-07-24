from fastapi import FastAPI, Request, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tempfile import NamedTemporaryFile
import os
import base64
from data import load_image, preprocess_image
from model import get_model
from inference import make_prediction, get_label_encoder

app = FastAPI()
templates = Jinja2Templates("templates")

@app.get("/", response_class = HTMLResponse)
def index(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("index.html", context)
    
    return response

@app.post("/result")
def show_image(request: Request, background_tasks: BackgroundTasks, input_image: UploadFile = File(...)):
    contents = input_image.file.read()
    encoded_image = base64.b64encode(contents).decode("utf-8")
    raw_image = load_image(contents)
    image = preprocess_image(raw_image)
    model = get_model()
    predicted_label, predicted_probability = make_prediction(model, image)

    context = {
        "request": request,
        "image": encoded_image,
        "predicted_label": predicted_label,
        "predicted_probability": f"{predicted_probability}%"
    }
    response = templates.TemplateResponse("result.html", context)
    return response

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8001)