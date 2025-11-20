import os
from pathlib import Path
from pydantic import BaseModel


class Settings(BaseModel):
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    embedding_model: str = "text-embedding-3-small"

    # Where to store FAISS + metadata files
    base_data_dir: Path = Path(__file__).resolve().parents[1] / "data"
    indexes_dir: Path = base_data_dir / "indexes"


config = Settings()
