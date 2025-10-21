import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is missing. Put it in your .env file.")
        return

    client = OpenAI(api_key=api_key)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a DVC course advisor assistant."},
                {"role": "user", "content": "Say: API connection successful."}
            ],
            temperature=0.2
        )
        print(resp.choices[0].message.content.strip())
    except Exception as e:
        print("API call failed:", e)

if __name__ == "__main__":
    main()
