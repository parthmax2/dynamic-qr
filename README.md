---
title: Dynamic-QR
emoji: 🔗
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
app_file: Dockerfile
pinned: false
---

# Dynamic-QR: QR Code Management System

<div align="center">

![Dynamic QR Logo](https://img.shields.io/badge/Dynamic--QR-green?style=for-the-badge&logo=qr-code&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Spaces-yellow.svg)](https://huggingface.co/spaces/parthmax/dynamic-qr)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*A powerful, FastAPI-based system for generating, updating, and tracking **dynamic QR codes** with enterprise-ready APIs.*

[🚀 Live Demo](https://huggingface.co/spaces/parthmax/dynamic-qr) • [📖 Documentation](#documentation) • [🛠️ Installation](#installation) • [📊 API Reference](#api-reference)

</div>

---

## 🌟 Overview

Dynamic-QR provides a **centralized system for creating and managing QR codes** that can be updated anytime without re-printing.  
It includes scan tracking, redirection logic, and a simple **web dashboard + API interface** for enterprise use cases.

---

## ✨ Key Features

### 🔗 **Dynamic QR Management**
- Create unique QR codes with short IDs  
- Update QR destination anytime without changing the QR image  
- Delete or deactivate codes when needed  

### 📊 **Analytics & Tracking**
- Track scan counts in real time  
- Log last scan timestamp  
- Manage activity status (`active/inactive`)  

### 🖥️ **Dashboard & APIs**
- Jinja2-powered dashboard to view all QR codes  
- REST APIs for integration with other systems  
- QR image generation endpoint for direct embedding  

### 🛡️ **Enterprise Ready**
- CORS enabled  
- Health check endpoint  
- Extensible for database or authentication integration  

---

## 🏗️ System Architecture

```

┌───────────────────┐     ┌────────────────────┐
│  Web Dashboard    │◄───►│   FastAPI Backend  │
│  (Jinja2)         │     │   (app.py)         │
└───────────────────┘     └─────────┬──────────┘
│
▼
┌───────────────────┐     ┌────────────────────┐
│  QR Generator     │     │   In-Memory Store  │
│  (qrcode lib)     │     │   (Dict, can use DB)│
└───────────────────┘     └────────────────────┘

````

---

## 🚀 Quick Start

### Option 1: Try Online (Recommended)
Visit the live demo: [🤗 HuggingFace Spaces](https://huggingface.co/spaces/parthmax/dynamic-qr)

### Option 2: Local Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/parthmax2/dynamic-qr.git
cd dynamic-qr
````

#### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

👉 Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🎯 Usage

### Web Dashboard

1. Open `/` to view all QR codes
2. Create a new QR by entering **title + redirect URL**
3. Update existing QR code targets anytime
4. Download the QR image and share

### API Examples

#### Create QR

```bash
curl -X POST "http://localhost:8000/create" \
  -F "title=My GitHub" \
  -F "redirect_url=https://github.com/parthmax2"
```

#### Redirect Scan

```bash
curl -i "http://localhost:8000/r/{qr_id}"
```

#### Get QR Image

```bash
curl -o qr.png "http://localhost:8000/qr/{qr_id}"
```

#### Get QR Metadata

```bash
curl "http://localhost:8000/api/qr/{qr_id}"
```

---

## 📚 API Reference

### Core Endpoints

| Method   | Endpoint          | Description          |
| -------- | ----------------- | -------------------- |
| `GET`    | `/`               | Dashboard UI         |
| `POST`   | `/create`         | Create new QR        |
| `POST`   | `/update/{qr_id}` | Update QR code       |
| `GET`    | `/r/{qr_id}`      | Redirect endpoint    |
| `GET`    | `/qr/{qr_id}`     | Get QR PNG image     |
| `DELETE` | `/delete/{qr_id}` | Delete QR code       |
| `GET`    | `/api/qr/{qr_id}` | Get QR metadata JSON |
| `GET`    | `/health`         | Health check         |

### Example QR Metadata Response

```json
{
  "id": "abc12345",
  "title": "My GitHub",
  "redirect_url": "https://github.com/parthmax2",
  "scan_count": 12,
  "created_at": "2025-08-31T10:45:00",
  "last_scanned": "2025-08-31T11:20:00",
  "is_active": true
}
```

---

## ⚙️ Configuration

### Environment Variables

| Variable   | Description                      | Default                                             |
| ---------- | -------------------------------- | --------------------------------------------------- |
| `BASE_URL` | Base URL used for QR redirection | `https://huggingface.co/spaces/parthmax/dynamic-qr` |

> ⚠️ In production, configure `BASE_URL` to match your deployment domain.

---

## 🛠️ Development

### Project Structure

```
dynamic-qr/
├── app.py                # Main FastAPI application
├── templates/            # Jinja2 templates (UI)
│   └── index.html
├── static/               # Static assets (CSS, JS)
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```


---

## 📊 Roadmap

* ✅ Dynamic QR CRUD
* ✅ Scan tracking
* 🔄 Persistent DB integration (SQLite/Postgres)
* 🔄 User authentication
* 🔄 Analytics dashboard with charts
* 🔄 Bulk QR generation & export

---

## 🔒 Security

* Input validation for URLs
* Configurable active/inactive state
* Ready for JWT auth integration
* Safe QR redirection logic

---

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Saksham Pathak** ([@parthmax2](https://github.com/parthmax2))
Generative AI Engineer | AI Apps & Developer Tools

---

<div align="center">

**[⭐ Star this repo](https://github.com/parthmax2/dynamic-qr)** if you find it useful!

Made with ❤️ by [parthmax](https://github.com/parthmax2)

</div>
```
