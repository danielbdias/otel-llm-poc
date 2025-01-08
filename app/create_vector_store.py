from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import json
import os
import time

import requests
from urllib.parse import quote

import config as app_config

from rag.vectorstore import save_vector_store

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

def encode_textfile_into_vector_store(trace_id : str, tracefile_path : str, config: app_config.Config):
    """
    Encodes a text file into a vector store using OpenAI embeddings.

    Args:
        tracefile_path: The path to the trace text file.
        output_file: The path where the vector store will be stored.
        chunk_size: The desired size of each text chunk.
        chunk_overlap: The amount of overlap between consecutive chunks.
    """

    text = ''

    # Load JSON file
    with open(tracefile_path, 'r') as file:
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

    save_vector_store(trace_id, config, cleaned_chunks)

def convert_trace_span_to_natural_language_text(trace_span) -> str:
  span_id = trace_span['spanID']
  operation_name = trace_span['operationName']
  duration = trace_span['duration']
  process_id = trace_span['processID']

  if len(trace_span['references']) > 0:
    parent_id = trace_span['references'][0]['spanID']
  else:
    parent_id = None

  description = [
    f"The span is named as '{operation_name}'",
    f"it has an id '{span_id}'",
    f"it has a duration of {duration}",
    f"it has a process id '{process_id}'",
  ]

  if parent_id is not None:
    description.append(f"it has a parent id '{parent_id}'")

  if len(trace_span['tags']) > 0:
    for tag in trace_span['tags']:
      description.append(f"it has a tag '{tag['key']} with value '{tag['value']}'")

  return ', '.join(description)

def convert_trace_process_to_natural_language_text(process_id : str, trace_process) -> str:
  service_name = trace_process['serviceName']

  description = [
    f"The process is named as '{service_name}'",
    f"it has an id '{process_id}'",
  ]

  if len(trace_process['tags']) > 0:
    for tag in trace_process['tags']:
      description.append(f"it has a tag '{tag['key']} with value '{tag['value']}'")

  return ', '.join(description)

def preprocess_trace_file(trace_id : str, trace_file : str, config: app_config.Config):
  preprocessed_trace_file = f"{config.vector_store_dir}/{trace_id}-preprocessed.txt"

  # Load Tracetest Trace file
  trace_data = None
  with open(trace_file, 'r') as file:
    trace_data = json.load(file)

  single_trace = trace_data[0]
  trace_spans = single_trace["spans"]
  trace_processes = single_trace["processes"]

  # Process each node and write it to the preprocessed trace file
  with open(preprocessed_trace_file, 'w') as file:
    for span in trace_spans:
      file.write(convert_trace_span_to_natural_language_text(span))
      file.write('\n')

    for process_id, process in trace_processes.items():
      file.write(convert_trace_process_to_natural_language_text(process_id, process))
      file.write('\n')

  return preprocessed_trace_file

def query_trace(trace_id : str, config: app_config.Config):
  # query Jaeger API to get trace data
# Construct the URL for Jaeger's HTTP API
    encoded_trace_id = quote(trace_id)
    url = f"{config.jaeger_api_url}/api/traces/{encoded_trace_id}"

    try:
        # Make the HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        jaeger_data = response.json()

        if not jaeger_data.get('data') or not jaeger_data['data']:
            raise Exception(f"Trace {trace_id} not found")

        # Save trace data to file
        output_file = f"{config.vector_store_dir}/{trace_id}.json"
        with open(output_file, 'w') as f:
            json.dump(jaeger_data['data'], f)

        return output_file

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to query Jaeger: {str(e)}")

def process_trace(trace_id : str, config: app_config.Config):
  start_time = time.time()

  # Just to avoid calling OpenAI API if the trace file already exists
  preexistent_trace_file = f"{config.vector_store_dir}/{trace_id}.json"
  if os.path.exists(preexistent_trace_file):
    return 0

  # Generate trace file
  trace_file = query_trace(trace_id, config)

  # Preprocess trace file
  preprocessed_trace_file = preprocess_trace_file(trace_id, trace_file, config)

  # Encode the preprocessed trace file into OpenAI embeddings and store in a vector store in disk
  encode_textfile_into_vector_store(trace_id, preprocessed_trace_file, config)

  elapsed_time = time.time() - start_time

  return elapsed_time
