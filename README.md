# Python RAG App Code Example

This project has the purpose of showing how to use the RAG model to generate answers for questions based on a given [OpenTelemetry](https://opentelemetry.io/) [Trace](https://opentelemetry.io/docs/concepts/signals/traces/).

To do that I'm splitting the project into two main parts:

- **Creating a Vector Store**: This part of the project is responsible for creating a vector store based on the trace data. To do that we preprocess the trace data to extract the necessary information and then we use the RAG model to generate the vectors for each trace span. The output of this part is a vector store that can be used to generate answers for questions based on the trace data.

- **Running the Chatbot**: This part of the project is responsible for running a chatbot that can answer questions based on the trace data. To do that we use the vector store created in the first part of the project to generate answers for the questions.

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
  make run/create-vector-store

  # run chatbot
  make run/chatbot
```
