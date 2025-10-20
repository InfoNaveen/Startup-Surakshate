import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(_file_)))
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import uvicorn
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response as StarletteResponse
from utils.security import SimpleRateLimiter

# Import API routes
from api.auth import router as auth_router
from api.scan import router as scan_router
from api.report import router as report_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Startup Surakshate",
    description="AI-powered cybersecurity platform for startups",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers + simple rate limiting middleware
rate_limiter = SimpleRateLimiter(limit=60, window_seconds=60)

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        # basic rate limit by client host
        client_ip = (request.client.host if request.client else "unknown")
        if not rate_limiter.allow(client_ip):
            return StarletteResponse("Too Many Requests", status_code=429)
        response: StarletteResponse = await call_next(request)
        # add minimal security headers
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response

app.add_middleware(SecurityMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(scan_router, prefix="/api/scan", tags=["Security Scans"])
app.include_router(report_router, prefix="/api/report", tags=["Reports"])

# Root route - serve the landing page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Dashboard route - serve the dashboard page
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
