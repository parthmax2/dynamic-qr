import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import qrcode

# In-memory redirect target
redirect_target = {"url": "https://www.example.com"}

app = FastAPI()

# Create QR code once
QR_PATH = "static/qr.png"
QR_ENDPOINT = "/qr"

def generate_qr_once():
    if not os.path.exists(QR_PATH):
        os.makedirs("static", exist_ok=True)
        img = qrcode.make(QR_ENDPOINT)
        img.save(QR_PATH)

generate_qr_once()

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.middleware("http")
async def update_redirect_target(request: Request, call_next):
    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "qr_url": "/static/qr.png",
        "current_url": redirect_target["url"]
    })

@app.get("/qr")
async def qr_redirect():
    return RedirectResponse(url=redirect_target["url"])

@app.post("/update")
async def update_link(new_url: str = Form(...)):
    redirect_target["url"] = new_url
    return RedirectResponse(url="/", status_code=303)
