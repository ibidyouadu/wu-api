from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates("templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("index.html", context)
    
    return response

@app.post("/transforminate")
def transforminate(request: Request, favnum: float = Form(...)):
    output = favnum/3.14159
    context = {"request": request, "output": output}
    response = templates.TemplateResponse("result.html", context)

    return response

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8001)