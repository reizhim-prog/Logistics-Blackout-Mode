import os
from pydantic import BaseModel

class Settings(BaseModel):
    DATA_DIR: str = os.getenv("DATA_DIR", os.path.join("..", "data", "processed"))
    TOP_N: int = int(os.getenv("TOP_N", "15"))

settings = Settings()
