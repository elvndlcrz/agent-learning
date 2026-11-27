from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from pydantic import BaseModel, Field
import time


load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

texts = [
    "Hi! It's Ana from Acme Corp. Text me at 0917-123-4567 or email ana@acme.com.",
    "This is Mark Reyes, freelance designer. Reach me: mark.reyes@gmail.com",
    "Call Jun at Globe Telecom, his number is +63 918 555 0199.",
    "hey its liza!! no email sorry, i work at jollibee haha",
    "Meeting notes: discussed Q3 budget. No contact info here.",
]

class Contact(BaseModel):
    name: str | None = Field(
        default=None,
        description="The person's name. Use null of no person is mentioned. Never invent a placeholder like 'Unknown'."
    )
    company: str | None = Field(
        default=None,
        description="The company or employer the person works for",
    )
    email: str | None
    phone: str | None

def extract_contact(text, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=f"Extract the contact details from this text:\n\n{text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Contact,
                ),
            )
            return response.parsed
        except errors.ServerError as e:
            wait = 2 ** attempt
            print(f"Server busy ({e.code}), retrying in {wait}s...")
            time.sleep(wait)
            attempt += 1
    raise RuntimeError("Gemini is still unavailable")

for text in texts:
    contact = extract_contact(text)
    print(f"Name: {contact.name or '-'} | Company: {contact.company or '-'} | Email: {contact.email or '-'} | Phone: {contact.phone or '-'}")