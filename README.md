# Agent Learning – Week 1

My first LLM projects using the Gemini API.

- chat.py: first API call, retries with exponential backoff
- chat_loop.py: streaming chatbot with memory, system prompt,
  token tracking, /reset and /cost commands
- extract.py: pulls contact details from messy text into
  structured JSON using a Pydantic schema

## Run it
1. Create a `.env` file with `GEMINI_API_KEY=your-key`
2. `pip install google-genai python-dotenv`
3. `python chat_loop.py`