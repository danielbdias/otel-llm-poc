from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from langchain_core.documents import Document

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_openai import ChatOpenAI

def encode_json(path, chunk_size=1000, chunk_overlap=200):
    """
    Encodes a JSON file into a vector store using OpenAI embeddings.

    Args:
        path: The path to the PDF file.
        chunk_size: The desired size of each text chunk.
        chunk_overlap: The amount of overlap between consecutive chunks.

    Returns:
        A FAISS vector store containing the encoded book content.
    """

    text = ''

    # Load JSON file
    with open(path, 'r') as file:
        text = file.read()

    document = Document(
        page_content=text,
        metadata={"source": "trace"},
    )

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=['\n']
    )
    chunks = text_splitter.split_documents([document])
    cleaned_chunks = replace_t_with_space(chunks)

    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(cleaned_chunks, embeddings)

    return vectorstore

def retrieve_context_per_question(question, chunks_query_retriever):
    """
    Retrieves relevant context and unique URLs for a given question using the chunks query retriever.

    Args:
        question: The question for which to retrieve context and URLs.

    Returns:
        A tuple containing:
        - A string with the concatenated content of relevant documents.
        - A list of unique URLs from the metadata of the relevant documents.
    """

    # Retrieve relevant documents for the given question
    docs = chunks_query_retriever.get_relevant_documents(question)

    # Concatenate document content
    # context = " ".join(doc.page_content for doc in docs)
    context = [doc.page_content for doc in docs]

    return context

def replace_t_with_space(list_of_documents):
    """
    Replaces all tab characters ('\t') with spaces in the page content of each document.

    Args:
        list_of_documents: A list of document objects, each with a 'page_content' attribute.

    Returns:
        The modified list of documents with tab characters replaced by spaces.
    """

    for doc in list_of_documents:
        doc.page_content = doc.page_content.replace('\t', ' ')  # Replace tabs with spaces
    return list_of_documents

def answer_question(openai_api_key, question, context):
  llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=openai_api_key
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
