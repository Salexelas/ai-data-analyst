import os
import requests
from dotenv import load_dotenv
from core.settings import LLMConfig
import time

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def call_llm(prompt: str, system_prompt: str = "You are a helpful AI") -> str:

    payload = {
        "model": LLMConfig.MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": LLMConfig.TEMPERATURE
    }

    start = time.time()

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=LLMConfig.TIMEOUT
    )

    duration = time.time() - start
    print(f"🔥 LLM RESPONSE TIME: {duration:.2f}s")

    if response.status_code != 200:
        raise Exception(response.text)

    result = response.json()

    return result["choices"][0]["message"]["content"]