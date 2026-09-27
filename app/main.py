import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import hotspots, alerts

# Create tables in DB
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fire Classification API",
    description="AI based industrial fire detection using NASA FIRMS",
    version="1.0.0"
)

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(hotspots.router, prefix="/api", tags=["Hotspots"])
app.include_router(alerts.router, prefix="/api", tags=["Alerts"])


@app.get("/")
def root():
    return {"message": "Fire Classification API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}