from typing import List

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.documents import Document

import config as app_config

def save_vector_store(config : app_config.Config, documents : List[Document]):
  """
  Creates a vector store based in a list of documents and saves it to disk.

  Args:
    config: The configuration object containing connection info to OpenAI API.
    documents: A list of document objects.
  """

  # Create embeddings and vector store
  embeddings = OpenAIEmbeddings(api_key=config.openai_api_key)
  vectorstore = FAISS.from_documents(documents, embeddings)

  # Store vector store in disk
  vectorstore.save_local(config.vector_store_dir, index_name=config.vector_store_index)

def load_vector_store(config : app_config.Config) -> FAISS:
  """
  Loads a vector store from disk.

  Args:
    config: The configuration object containing connection info to OpenAI API.
    output_dir: The directory where the vector store is saved.
    output_index: The name of the index to be loaded.
  """

  # Load vector store from disk
  embeddings = OpenAIEmbeddings(api_key=config.openai_api_key)
  return FAISS.load_local(config.vector_store_dir, embeddings, index_name=config.vector_store_index, allow_dangerous_deserialization=True)
