# Python RAG App Code Example

TBD

### Creating a Vector Store

```sh
python ./app/create_vector_store.py --trace-file=/Users/danielbdias/Development/Repositories/work/code-examples-python-rag-app/data/trace.json --preprocessed-trace-file=/Users/danielbdias/Development/Repositories/work/code-examples-python-rag-app/data/trace-description.txt --output-dir=/Users/danielbdias/Development/Repositories/work/code-examples-python-rag-app/data --output-index=vectorstore
```

### Running example locally

#### Setting up the environment

```bash

# create venv
python -m venv ./_venv

# activate env
source _venv/bin/activate

# install requirements
pip install -r requirements.txt

# add openai api key
echo "OPENAI_API_KEY={your-open-ai-api-key}" >> .env
```
