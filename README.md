# Agent Learning – Week 1

My first LLM projects using the Gemini API.

- `chat.py`: first API call, plus retries with exponential backoff
- `chat_loop.py`: terminal chatbot with conversation memory

## Run it
1. Create a `.env` file with `GEMINI_API_KEY=your-key`
2. `pip install google-genai python-dotenv`
3. `python chat_loop.py`