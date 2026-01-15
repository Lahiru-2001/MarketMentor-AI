from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(BASE_DIR, "assets")),
    name="assets",
)


app.mount(
    "/default_pages",
    StaticFiles(directory=os.path.join(BASE_DIR, "default_pages")),
    name="default_pages",
)


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


from backend.api.routes.auth import router as auth_router

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)
