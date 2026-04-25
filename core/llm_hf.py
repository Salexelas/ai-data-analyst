import requests
import os

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

def call_hf(prompt: str):

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=3
    )

    if response.status_code != 200:
        raise Exception("HF error")

    result = response.json()

    return result[0]["generated_text"]