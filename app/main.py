import sys
import os
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
from routes import hotspots, alerts

def bg_fetch():
    try:
        from services.firms_fetch import fetch_and_store
        print("Auto-fetching hotspots on startup...")
        fetch_and_store()
        print("Startup fetch complete!")
    except Exception as e:
        print(f"Startup fetch failed: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=bg_fetch, daemon=True).start()
    yield

# Create tables in DB
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fire Classification API",
    description="AI based industrial fire detection using NASA FIRMS",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hotspots.router, prefix="/api", tags=["Hotspots"])
app.include_router(alerts.router, prefix="/api", tags=["Alerts"])

@app.get("/")
def root():
    return {"message": "Fire Classification API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}