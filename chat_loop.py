from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
import time

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

SYSTEM = """You are a friendly Python tutor for beginners.

Task: Help the user learn and understand Python.

Rules:
- Only answer questions about Python and programming.
- If a question is not about Python, politely say you can only help with Python, then suggest a Python topic instead.
- Keep answers to 3 sentences or fewer unless the user asks for more detail.
- Use simple words.

Format: When it helps, include one short code example."""

def stream_reply(contents, retries=3):
    attempt = 0
    while attempt < retries:
        full_reply = ""
        last_chunk = None
        try:
            stream = client.models.generate_content_stream(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM,
                    max_output_tokens=500,
                ),
            )
            for chunk in stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_reply += chunk.text
                last_chunk = chunk
            print()  # move to a new line after the reply
            return full_reply, last_chunk
        except errors.ServerError as e:
            if full_reply:
                # text was already shown, so don't retry and repeat it
                print("\n(Connection problem, the answer was interrupted.)")
                return full_reply, last_chunk
            wait = 2 ** attempt
            print(f"Server busy ({e.code}), retrying in {wait}s...")
            time.sleep(wait)
            attempt += 1
    raise RuntimeError("Gemini is still unavailable")

messages = []
turn = 0
total_tokens = 0
while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue

    if user_input.lower() in {"quit", "exit"}:
        break
    elif user_input.lower() == "/reset":
        turn = 0
        messages = []
        print("Conversation cleared.")
        continue
    elif user_input.lower() == "/cost":
        print(f"Total tokens used so far: {total_tokens}")
        continue
    messages.append({"role": "user", "parts": [{"text": user_input}]})
    print(f"[Turn {turn + 1}] Gemini: ", end="", flush=True)
    try:
        reply, last_chunk = stream_reply(messages)
    except RuntimeError as e:
        print(e)
        messages.pop()
        continue
    turn += 1
    usage = last_chunk.usage_metadata
    total_tokens += usage.total_token_count
    print(f"(tokens: {usage.prompt_token_count} in, {usage.candidates_token_count} out)")

    if last_chunk.candidates[0].finish_reason.name == "MAX_TOKENS":
        print("(Warning: answer was cut off. Ask me to continue.)")