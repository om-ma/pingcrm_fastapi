from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.middleware import error_handler
from app.api.v1.api import api_router
import os

app = FastAPI(title="PingCRM API")

# Configure CORS
origins = [
    "https://pingcrm-reactjs.onrender.com",  # Production React frontend
    "http://localhost:3000",  # Local React frontend
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(error_handler)
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)