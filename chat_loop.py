from dotenv import load_dotenv
from google import genai
from google.genai import errors
import time

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

def ask(contents, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            response = client.models.generate_content(model=MODEL, contents=contents)
            return response.text
        except errors.ServerError as e:
            wait = 2 ** attempt
            print(f"Server busy ({e.code}), retrying in {wait}s...")
            time.sleep(wait)
            attempt += 1
    raise RuntimeError("Gemini is still unavailable")

messages = []
while True:
    user_input = input("You: ")
    if user_input.lower() in {"quit", "exit"}:
        break
    messages.append({"role": "user", "parts": [{"text": user_input}]})
    try:
        reply = ask(messages)
    except RuntimeError as e:
        print(e)
        messages.pop()
        continue
    messages.append({"role": "model", "parts": [{"text": reply}]})
    print("Gemini: ", reply)