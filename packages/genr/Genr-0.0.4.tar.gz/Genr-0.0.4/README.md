# Genr

This is a python package built on top of OpenAI's language API, designed to perform various tasks such as summarization, Q&A preparation, text-to-dialogue conversion, NER, and more.

## Features

| Feature | Status |
| --- | --- |
| Text Summarization | Implemented |
| Question and Answer Preparation | Implemented |
| Text-to-Dialogue Conversion | Implemented |
| Named Entity Recognition (NER) | Implemented |
| Text Generation | Implemented |
| Translation | Pending |

## Getting Started

To use this package, you need to sign up for an API key from OpenAI to access their language API.

1. Clone the repository to your local machine:

 ```bash
 git clone https://github.com/psytech42/genr.ai/
 ```
 

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Use the package in your code:

```python
import genr

# Initialize the API with your API key
openai = genr("YOUR_API_KEY")

# Use the desired function to perform the task
result = openai.summarize("Your text here")

print(result)
```


