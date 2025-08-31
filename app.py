from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import qrcode
import io
import uuid
from typing import Dict, Optional
import json
from datetime import datetime, timedelta
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Dynamic QR Generator",
    description="Enterprise-grade dynamic QR code management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory storage for QR codes (use database in production)
qr_codes: Dict[str, Dict] = {}

class QRCodeManager:
    """Middleware class for QR code management logic"""
    
    @staticmethod
    def generate_qr_id() -> str:
        """Generate unique QR code identifier"""
        return str(uuid.uuid4())[:8]
    
    @staticmethod
    def create_qr_code(qr_id: str, redirect_url: str, title: str = "Untitled") -> Dict:
        """Create a new QR code entry"""
        qr_data = {
            "id": qr_id,
            "title": title,
            "redirect_url": redirect_url,
            "scan_count": 0,
            "created_at": datetime.now().isoformat(),
            "last_scanned": None,
            "is_active": True
        }
        qr_codes[qr_id] = qr_data
        return qr_data
    
    @staticmethod
    def update_qr_code(qr_id: str, redirect_url: str, title: str = None) -> Optional[Dict]:
        """Update existing QR code"""
        if qr_id not in qr_codes:
            return None
        
        qr_codes[qr_id]["redirect_url"] = redirect_url
        if title:
            qr_codes[qr_id]["title"] = title
        qr_codes[qr_id]["updated_at"] = datetime.now().isoformat()
        return qr_codes[qr_id]
    
    @staticmethod
    def get_qr_code(qr_id: str) -> Optional[Dict]:
        """Get QR code data"""
        return qr_codes.get(qr_id)
    
    @staticmethod
    def increment_scan_count(qr_id: str) -> None:
        """Increment scan count and update last scanned time"""
        if qr_id in qr_codes:
            qr_codes[qr_id]["scan_count"] += 1
            qr_codes[qr_id]["last_scanned"] = datetime.now().isoformat()
    
    @staticmethod
    def get_all_qr_codes() -> Dict[str, Dict]:
        """Get all QR codes"""
        return qr_codes
    
    @staticmethod
    def generate_qr_image(qr_id: str) -> io.BytesIO:
        """Generate QR code image"""
        base_url = os.getenv("BASE_URL", "https://huggingface.co/spaces/parthmax/dynamic-qr")
        qr_url = f"{base_url}/r/{qr_id}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io

# Initialize QR manager
qr_manager = QRCodeManager()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main dashboard page"""
    all_qr_codes = qr_manager.get_all_qr_codes()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "qr_codes": all_qr_codes
    })

@app.post("/create")
async def create_qr(
    title: str = Form(...),
    redirect_url: str = Form(...),
):
    """Create a new QR code"""
    if not redirect_url.startswith(('http://', 'https://')):
        redirect_url = f"https://{redirect_url}"
    
    qr_id = qr_manager.generate_qr_id()
    qr_data = qr_manager.create_qr_code(qr_id, redirect_url, title)
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/update/{qr_id}")
async def update_qr(
    qr_id: str,
    title: str = Form(...),
    redirect_url: str = Form(...),
):
    """Update existing QR code"""
    if qr_id not in qr_codes:
        raise HTTPException(status_code=404, detail="QR code not found")
    
    if not redirect_url.startswith(('http://', 'https://')):
        redirect_url = f"https://{redirect_url}"
    
    qr_manager.update_qr_code(qr_id, redirect_url, title)
    return RedirectResponse(url="/", status_code=303)

@app.get("/r/{qr_id}")
async def redirect_qr(qr_id: str):
    """Redirect endpoint for QR code scans"""
    qr_data = qr_manager.get_qr_code(qr_id)
    
    if not qr_data or not qr_data.get("is_active"):
        raise HTTPException(status_code=404, detail="QR code not found or inactive")
    
    # Increment scan count
    qr_manager.increment_scan_count(qr_id)
    
    return RedirectResponse(url=qr_data["redirect_url"])

@app.get("/qr/{qr_id}")
async def get_qr_image(qr_id: str):
    """Generate and serve QR code image"""
    if qr_id not in qr_codes:
        raise HTTPException(status_code=404, detail="QR code not found")
    
    img_io = qr_manager.generate_qr_image(qr_id)
    return StreamingResponse(img_io, media_type="image/png")

@app.delete("/delete/{qr_id}")
async def delete_qr(qr_id: str):
    """Delete QR code"""
    if qr_id not in qr_codes:
        raise HTTPException(status_code=404, detail="QR code not found")
    
    del qr_codes[qr_id]
    return {"message": "QR code deleted successfully"}

@app.get("/api/qr/{qr_id}")
async def get_qr_data(qr_id: str):
    """Get QR code data via API"""
    qr_data = qr_manager.get_qr_code(qr_id)
    if not qr_data:
        raise HTTPException(status_code=404, detail="QR code not found")
    return qr_data

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)