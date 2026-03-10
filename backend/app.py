import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api.routes.recommendation import router as rec_router
from api.routes.auth import router as auth_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routes.recommendation import router as rec_router
from api.routes.auth import router as auth_router
from api.routes.support import router as support_router
from api.routes.profile import router as profile_router
from api.routes.admin import router as admin_router
import os



app = FastAPI(
    title="MarketMentor-AI",
    description="AI-powered financial recommendation system",
    version="1.0.0"
)


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
    name="assets"
)

app.mount(
    "/default_pages",
    StaticFiles(directory=os.path.join(BASE_DIR, "default_pages")),
    name="default_pages"
)


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)


@app.get("/")
def serve_index():
    """
    Serve the main index.html page
    """
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "MarketMentor-AI backend is running"}

# ---------------- API ROUTERS ----------------
app.include_router(auth_router, prefix="/auth")
app.include_router(rec_router, prefix="/recommendation")
app.include_router(support_router, prefix="/support", tags=["Support"])
app.include_router(profile_router, prefix="/profile")
app.include_router(admin_router, prefix="/admin", tags=["Admin"])