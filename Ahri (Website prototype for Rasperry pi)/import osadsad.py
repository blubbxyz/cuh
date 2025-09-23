import os
from openai import OpenAI
from dotenv import load_dotenv
import time
from openai import OpenAI, OpenAIError

# Lade die ahrigpt.env Datei
env_path = r"D:/i guess/cuh/Ahri (Website prototype for Rasperry pi)/ahrigpt.env"
load_dotenv(env_path)

# API-Key auslesen
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️ Kein API-Key gefunden! Bitte ahrigpt.env prüfen oder Umgebungsvariable setzen.")
    exit()
else:
    print("✅ API-Key gefunden:", api_key[:5] + "...")  # nur die ersten 5 Zeichen

# OpenAI Client erstellen
client = OpenAI(api_key=api_key)
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)