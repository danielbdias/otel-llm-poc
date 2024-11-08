from typing import List

from langchain_core.documents import Document

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_openai import ChatOpenAI
from langchain_core.vectorstores.base import VectorStoreRetriever

import config as app_config

def retrieve_context_per_question(question : str, chunks_query_retriever : VectorStoreRetriever) -> List[str]:
    """
    Retrieves relevant context and unique URLs for a given question using the chunks query retriever.

    Args:
        question: The question for which to retrieve context and URLs.

    Returns:
        A list containing content of relevant documents.
    """

    # Retrieve relevant documents for the given question
    docs = chunks_query_retriever.get_relevant_documents(question)

    # Get relevant content
    context = [doc.page_content for doc in docs]

    return context

def answer_question(config : app_config.Config, question : str, context : List[str]):
  llm = ChatOpenAI(
    model=config.gpt_model,
    openai_api_key=config.openai_api_key
  )

  # Define prompt
  prompt = ChatPromptTemplate.from_messages(
      [("system", "Given the following context:\\n\\n{context}\n\nAnswer the following question: {question}")]
  )

  # Instantiate chain
  chain = create_stuff_documents_chain(llm, prompt)

  # Limit to 3 documents
  docs = [Document(page_content=t) for t in context[:3]]

  # Invoke chain
  return chain.invoke({"context": docs, "question": question})
