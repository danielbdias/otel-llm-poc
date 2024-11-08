# Python RAG App Code Example

This project has the purpose of showing how to use the RAG model to generate answers for questions based on a given [OpenTelemetry](https://opentelemetry.io/) [Trace](https://opentelemetry.io/docs/concepts/signals/traces/).

The chatbot was inspired by [Streamlit Chatbot example](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py).

To do that I'm splitting the project into two main parts:

- **Creating a Vector Store**: This part of the project is responsible for creating a vector store based on the trace data. To do that we preprocess the trace data to extract the necessary information and then we use the RAG model to generate the vectors for each trace span. The output of this part is a vector store that can be used to generate answers for questions based on the trace data.

- **Running the Chatbot**: This part of the project is responsible for running a chatbot that can answer questions based on the trace data. To do that we use the vector store created in the first part of the project to generate answers for the questions.

Here is a short video showing how the chatbot works:
<div style="position: relative; padding-bottom: 56.36743215031315%; height: 0;">
  <iframe src="https://www.loom.com/embed/6570154088a942268a30c60dee9dec96?sid=0203203c-dff1-442e-bd38-0b3ceea42c9a" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
  </iframe>
</div>

### Setting up the project

First of all, you need to have an OpenAI API Key to use the project, you can get one [here](https://platform.openai.com/signup).

Then, just create a `.env` file in the root of the project with the following content:

```sh
  # add openai api key
  echo "OPENAI_API_KEY={your-open-ai-api-key}" >> .env
```

Also, I'm considering that you have Python 3.12 installed in your machine. Otherwise, you can download it [here](https://www.python.org/downloads/).

#### Creating a virtual env and downloading the dependencies

You will create a virtual env to have a clean environment to run the project, by executing the following commands:

```sh
  # create venv
  python -m venv ./_venv

  # activate env
  source _venv/bin/activate

  # install requirements
  pip install -r requirements.txt
```

#### Running the use cases

To create the VectorStore and run the chatbot you can use the following commands:

```sh
  # create vector store
  python ./app/create_vector_store.py --trace-file=$PWD/data/trace.json --preprocessed-trace-file=$PWD/data/trace-description.txt

  # run chatbot
  streamlit run ./app/streamlit_app.py
```
