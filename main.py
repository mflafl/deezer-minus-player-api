from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from mzapi.routes.tracks import router as tracks_routes
from mzapi.routes.jobs import router as jobs_routes

app = FastAPI(debug=True)

app.include_router(tracks_routes)
app.include_router(jobs_routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}
