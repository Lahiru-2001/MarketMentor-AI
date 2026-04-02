import sys
import os

# Add the current file's directory to sys.path to allow relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# FastAPI core and utilities
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # Serve static files like JS, CSS, images
from fastapi.responses import FileResponse   # Send files as HTTP responses
from fastapi.middleware.cors import CORSMiddleware  # Handle Cross-Origin Resource Sharing (CORS)

# Import route modules
from api.routes.recommendation import router as rec_router
from api.routes.auth import router as auth_router
from api.routes.support import router as support_router
from api.routes.profile import router as profile_router
from api.routes.admin import router as admin_router


# Initialize FastAPI application with metadata
app = FastAPI(
    title="MarketMentor-AI",
    description="AI-powered financial recommendation system",
    version="1.0.0"
)

# Enable CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (can restrict in production)
    allow_credentials=True,     # Allow cookies, authentication headers
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all HTTP headers
)

# Base directory of the project (one level up from current file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Serve static assets from /assets URL
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(BASE_DIR, "assets")),
    name="assets"
)

# Serve default HTML pages from /default_pages URL
app.mount(
    "/default_pages",
    StaticFiles(directory=os.path.join(BASE_DIR, "default_pages")),
    name="default_pages"
)

# Include routers for modular route handling
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(rec_router, prefix="/recommendation", tags=["Recommendation"])
app.include_router(support_router, prefix="/support", tags=["Support"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


# Serve the main frontend index.html at the root URL
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# Health check endpoint to verify backend is running
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "MarketMentor-AI backend is running"
    }