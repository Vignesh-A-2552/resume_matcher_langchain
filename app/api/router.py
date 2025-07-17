from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.vector_service import VectorService
from app.services.matching_service import MatchingService
from app.utils.file_utils import extract_text_and_name
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
vector_service = VectorService()
matching_service = MatchingService()


@router.post("/upload")
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


@router.post("/match")
async def search_match(jdfile: UploadFile = File(...)):
    try:
        jd_text, _ = extract_text_and_name(jdfile)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    if not jd_text:
        return JSONResponse(status_code=400, content={"error": "The uploaded JD file is empty or unreadable."})

    try:
        resumes = vector_service.search_similar_resumes(jd_text, k=3)
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to load vector store or perform search."})

    if not resumes:
        return JSONResponse(status_code=400, content={"error": "No resumes available in the vector store."})

    matches = matching_service.generate_matches(resumes, jd_text)
    return {"matches": matches}