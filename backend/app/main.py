from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import story

app = FastAPI(title="AI Audio Storyteller", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/audio", StaticFiles(directory="data/audio"), name="audio")

app.include_router(story.router, prefix="/api", tags=["story"])

@app.get("/")
async def root():
    return {"message": "AI Audio Storyteller API"}