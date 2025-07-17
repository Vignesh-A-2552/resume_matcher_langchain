import os
import shutil
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import TextLoader


def extract_text_and_name(file: UploadFile) -> tuple[str, str]:
    """Extract text content and filename from uploaded file."""
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported.")

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        loader = TextLoader(temp_path)
        documents = loader.load()
        text = documents[0].page_content if documents else ""
        name = file.filename.rsplit(".", 1)[0]
    finally:
        os.remove(temp_path)

    return text.strip(), name