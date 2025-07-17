import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    BASE_URL: str = os.getenv('BASE_URL')
    MODEL: str = os.getenv('MODEL')
    VECTOR_STORE_PATH: str = "vector_store"
    EMBEDDINGS_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]


settings = Settings()