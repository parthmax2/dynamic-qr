from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import qrcode

# Initialize FastAPI app
app = FastAPI()

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Default redirection URL (can be modified)
redirect_target = {
    "url": "https://www.example.com"
}

# Ensure QR image is generated
def generate_qr():
    url = "https://dynamic-qr-yidr.onrender.com/qr"
    qr_img = qrcode.make(url)
    os.makedirs("static", exist_ok=True)
    qr_img.save("static/qr.png")

generate_qr()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "qr_url": "/static/qr.png",
        "current_url": redirect_target["url"]
    })

@app.get("/qr")
async def qr_redirect():
    # Always redirect to the current URL
    return RedirectResponse(url=redirect_target["url"])

@app.post("/update")
async def update_link(new_url: str = Form(...)):
    # Update the redirection target
    redirect_target["url"] = new_url
    return RedirectResponse(url="/", status_code=303)
