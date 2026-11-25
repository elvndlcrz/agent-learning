from dotenv import load_dotenv
from google import genai
from google.genai import errors
import time

load_dotenv()
client = genai.Client()
MODEL = "gemini-4-hydrogen"

def ask(contents, retries=3):
    for attempt in range(retries):
        try:
            r1 = client.models.generate_content(model=MODEL, contents=contents)
            return r1.text
        except errors.ServerError as e:
            wait = 2 ** attempt
            print(f"Server busy ({e.code}), retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Gemini is still unavailable. Try again later.")

print("Reply 1:", ask("My name is Sylver"))
print("Reply 2:", ask("What is my name?"))