from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.middleware import error_handler
from app.api.v1.api import api_router

app = FastAPI(title="PingCRM API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handling middleware
app.middleware("http")(error_handler)

# Include API router
app.include_router(api_router, prefix="/api/v1")
