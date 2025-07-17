from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.vector_service import VectorService
from app.utils.file_utils import extract_text_and_name
import loguru

api = APIRouter()
vector_service = VectorService()

logger = loguru.logger

@api.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        resume_text, name = extract_text_and_name(file)
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return JSONResponse(status_code=400, content={"error": str(e)})

    if not resume_text:
        return JSONResponse(status_code=400, content={"error": "The uploaded file is empty or unreadable."})

    try:
        vector_service.add_resume(resume_text, name)
    except Exception as e:
        logger.error(f"Vector DB error: {e}")
        return JSONResponse(status_code=500, content={"error": f"Failed to store resume: {str(e)}"})

    logger.info(f"Uploaded resume for: {name}")
    return {"message": f"Resume for {name} added to vector store."}