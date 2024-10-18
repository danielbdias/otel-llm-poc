## TBD

TBD

### Running example locally

#### Setting up the environment

```bash

# create venv
python -m venv ./_venv

# activate env
source _venv/bin/activate

# install requirements
pip install -r app/requirements.txt

# install OTel auto-instrumentation
opentelemetry-bootstrap -a install

# add openai api key
echo "OPENAI_API_KEY={your-open-ai-api-key}" >> .env
# add google gemini api key (optional)
echo "GOOGLE_API_KEY={your-google-gemini-api-key}" >> .env
```