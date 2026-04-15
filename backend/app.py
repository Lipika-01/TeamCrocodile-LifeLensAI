"""
LifeLensAI: Clinical Predictive Intelligence Platform
Main Entry Point

This module initializes the FastAPI application, configures security middlewares (CORS),
and aggregates the diagnostic core routers including Authentication, Tabular Prediction,
and Medical Imaging Analysis.

Architecture: Enterprise-grade Microservices Approach
Author: LifeLensAI Engineering Team
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from routes import api, auth, imaging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LifeLensAI Diagnostic Core",
    description="High-fidelity predictive analytics for early-stage disease detection using clinical markers and imaging data.",
    version="1.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS for multi-tier deployment (Frontend on Vercel, Backend on Render)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5500,http://127.0.0.1:5500").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """System health monitor for deployment status."""
    return {"status": "healthy", "timestamp": str(os.getenv("VERCEL_GIT_COMMIT_SHA", "local"))}

from fastapi.staticfiles import StaticFiles
import os

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(api.router, prefix="/api", tags=["Predict"])
app.include_router(imaging.router, prefix="/api", tags=["Imaging"])

# Serve static files from the frontend directory (climb out of backend)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
