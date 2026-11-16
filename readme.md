# Chabot Zev Gemini

An AI-first customer support bot built with TypeSafe's Jev and Google's Gemini API.

It leverages a knowledge base of common issues and their resolutions to automatically assist users and resolve requests whenever possible, while they wait for a human support operator to become available. 

Rather than forcing users through a series of AI-only troubleshooting steps before granting access to human assistance, the bot provides immediate, AI-powered support in parallel with the human support queue.  
This approach helps reduce waiting times by resolving straightforward issues automatically while ensuring users never have to exhaust automated options before getting human help.

## Local running

Create a `.env` file in the project directory with your
[Gemini API key](https://aistudio.google.com/apikey):

```text
GEMINI_API_KEY=your_api_key_here
```

Install the dependencies and start the application:

```bash
# Create a virtual environment (only once).
python3 -m venv ./my-env

# Activate the virtual environment.
source ./my-env/bin/activate

# Install dependencies (only once).
python -m pip install -r requirements.txt

# Start the application.
python main.py
```
