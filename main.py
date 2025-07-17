import loguru
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import match_api, upload_api

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Configure logging
loguru.logger.add("file.log", rotation="1 MB")
logger = loguru.logger

# Include API routes
app.include_router(upload_api, prefix="/upload")
app.include_router(match_api, prefix="/match")


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
