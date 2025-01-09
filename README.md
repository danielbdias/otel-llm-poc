# Python RAG App Code Example

This project has the purpose of showing how to use the RAG model to generate answers for questions based on a given [OpenTelemetry](https://opentelemetry.io/) [Traces](https://opentelemetry.io/docs/concepts/signals/traces/).

The chatbot was inspired by [Streamlit Chatbot example](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py).

### Setting up the project

First of all, you need to have an OpenAI API Key to use the project, you can get one [here](https://platform.openai.com/signup).

Then, just create a `.env` file in the root of the project with the following content:

```sh
  # add openai api key
  echo "OPENAI_API_KEY={your-open-ai-api-key}" >> .env
```

Also, I'm considering that you have `Python 3.12` and `uv` installed in your machine. Otherwise, you can download it here:

- Python 3.12: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- `uv`: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

#### Creating a virtual env and downloading the dependencies

You will create a virtual env to have a clean environment to run the project, by executing the following commands:

```sh
  # create venv and install dependencies
  uv sync

  # activate venv
  source .venv/bin/activate
```

#### Running the use cases

To create the VectorStore and run the chatbot you can use the following commands:

```sh
  # create vector store
  python ./app/create_vector_store.py --trace-file=$PWD/data/trace.json --preprocessed-trace-file=$PWD/data/trace-description.txt

  # run chatbot
  streamlit run ./app/streamlit_app.py
```
