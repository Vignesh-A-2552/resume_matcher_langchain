import os
import loguru
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

logger = loguru.logger


class VectorService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDINGS_MODEL)
        self.vector_store_path = settings.VECTOR_STORE_PATH

    def add_resume(self, resume_text: str, name: str):
        """Add a resume to the vector store."""
        try:
            if os.path.exists(self.vector_store_path):
                db = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
                db.add_texts([resume_text], metadatas=[{"name": name}])
            else:
                db = FAISS.from_texts([resume_text], self.embeddings, metadatas=[{"name": name}])
            db.save_local(self.vector_store_path)
        except Exception as e:
            logger.error(f"Error adding resume to vector store: {e}")
            raise

    def search_similar_resumes(self, jd_text: str, k: int = 3) -> list:
        """Search for similar resumes based on job description."""
        if not os.path.exists(self.vector_store_path):
            return []

        try:
            db = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
            jd_vector = self.embeddings.embed_query(jd_text)
            results = db.similarity_search_by_vector(jd_vector, k=k)
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            raise