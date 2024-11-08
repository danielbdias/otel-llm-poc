from dataclasses import dataclass
from dotenv import load_dotenv

import os

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
  openai_api_key: str = ""
  gpt_model: str = "gpt-4o-mini"
  vector_store_chunk_size: int = 1000
  vector_store_chunk_overlap: int = 200
  vector_store_dir: str = "./data"
  vector_store_index: str = "vectorstore"

def get_config() -> Config:
  api_key = os.getenv("OPENAI_API_KEY", "")
  if api_key == "":
    raise ValueError("OPENAI_API_KEY key not found in environment variables")

  return Config(
    openai_api_key=api_key,
  )
