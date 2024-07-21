from fastapi import FastAPI, Request, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tempfile import NamedTemporaryFile
import os
import base64

app = FastAPI()
templates = Jinja2Templates("templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("index.html", context)
    
    return response

@app.post("/result")
def show_image(request: Request, background_tasks: BackgroundTasks, input_image: UploadFile = File(...)):
    contents = input_image.file.read()
    encoded_image = base64.b64encode(contents).decode("utf-8")
    
    context = {"request": request, "image": encoded_image}
    response = templates.TemplateResponse("result.html", context)
    return response

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8001)