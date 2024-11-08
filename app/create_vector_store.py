from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import argparse
import json
import time

import config as app_config
from rag.vectorstore import save_vector_store

config = app_config.get_config()

def replace_t_with_space(list_of_documents : List[Document]) -> List[Document]:
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

def encode_textfile_into_vector_store(path : str, config: app_config.Config):
    """
    Encodes a text file into a vector store using OpenAI embeddings.

    Args:
        path: The path to the text file.
        output_file: The path where the vector store will be stored.
        chunk_size: The desired size of each text chunk.
        chunk_overlap: The amount of overlap between consecutive chunks.
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
        chunk_size=config.vector_store_chunk_size,
        chunk_overlap=config.vector_store_chunk_overlap,
        length_function=len,
        separators=['\n']
    )
    chunks = text_splitter.split_documents([document])
    cleaned_chunks = replace_t_with_space(chunks)

    save_vector_store(config, cleaned_chunks)

def convert_node_data_to_text(node_data) -> str:
  """
    Converts a node data (trace span) object to a natural language description.

    Args:
        node_data: Dictionary containing the node data (trace span).

    Returns:
        A string describing the node data in natural language.
  """

  description = [
    f"The node is named as '{node_data['name']}'",
    f"it has an id '{node_data['id']}'",
    f"it has a '{node_data['kind']}' kind",
    f"it has a duration of {node_data['attributes']['tracetest.span.duration']}",
  ]

  if 'parent_id' in node_data:
    description.append(f"it has a parent id '{node_data['parentId']}'")

  if 'tracetest.span.type' in node_data['attributes']:
    description.append(f"it has a '{node_data['attributes']['tracetest.span.type']}' span type")

  return ', '.join(description)

def preprocess_trace_file(trace_file : str, preprocessed_trace_file : str):
  """
    Preprocesses a Tracetest trace file into a file containing each node (span) described in natural language description.

    Args:
        trace_file: Path to the trace JSON file.
        preprocessed_trace_file: Path where the preprocessed trace descripted in natural language will be stored.
  """
  # Load Tracetest Trace file
  trace_data = None
  with open(trace_file, 'r') as file:
    trace_data = json.load(file)

  flat_representation = trace_data["flat"]

  # Process each node and write it to the preprocessed trace file
  with open(preprocessed_trace_file, 'w') as file:
    for node_id in flat_representation.keys():
      file.write(convert_node_data_to_text(flat_representation[node_id]))
      file.write('\n')

##################################################################
# Script start
##################################################################

parser = argparse.ArgumentParser(description='Process Tracetest trace data in JSON and store it as a LangChain VectorStore.')

parser.add_argument('--trace-file', type=str, required=True, help='Path to the trace JSON file')
parser.add_argument('--preprocessed-trace-file', type=str, required=True, help='Path where the preprocessed trace descripted in natural language will be stored')

args = parser.parse_args()
trace_file = args.trace_file
preprocessed_trace_file = args.preprocessed_trace_file

start_time = time.time()

print('Starting process...\n')

print('Preprocessing trace file...')

# Step 1: Preprocess the trace file
preprocess_trace_file(trace_file, preprocessed_trace_file)

print('Done!\n\n')

print('Encoding preprocessed trace file into vector store...')

# Step 2: Encode the preprocessed trace file into OpenAI embeddings and store in a vector store in disk
encode_textfile_into_vector_store(preprocessed_trace_file, config)

print('Done!\n\n')

elapsed_time = time.time() - start_time
print(f'Elapsed time: {elapsed_time} seconds')
