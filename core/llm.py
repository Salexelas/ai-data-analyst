import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def call_llm(prompt: str) -> str:
    """
    Llama al modelo de Hugging Face y devuelve texto generado.
    """

    if not API_KEY:
        raise ValueError("Falta HUGGINGFACE_API_KEY en .env")

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.2,
            "return_full_text": False  # 🔥 clave para evitar que repita el prompt
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    # Debug opcional
    # print("HF response:", result)

    try:
        return result[0]["generated_text"].strip()
    except Exception:
        return str(result)