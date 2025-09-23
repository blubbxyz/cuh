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

def chat_with_gpt(prompt):
    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}]
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            if "insufficient_quota" in str(e) or "RateLimitError" in str(e):
                print("⏳ Rate Limit / Quota erreicht, warte 5 Sekunden...")
                time.sleep(5)
            else:
                raise e

if __name__ == "__main__":
    while True:
        user_input = input("Du: ")
        if user_input.lower() in ["exit", "quit", "stop"]:
            break
        answer = chat_with_gpt(user_input)
        print("ChatGPT:", answer)

