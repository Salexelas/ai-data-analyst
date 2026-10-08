'''import os
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

    return result["choices"][0]["message"]["content"]'''


import os
import time
import requests
from dotenv import load_dotenv
from core.settings import LLMConfig

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Tarifas de referencia para GPT-OSS-120B en Groq.
# Verificá las tarifas vigentes antes de usar estos valores en producción.
PRICING_PER_MILLION = {
    "openai/gpt-oss-120b": {
        "input": 0.15,
        "output": 0.60,
    }
}


def call_llm(prompt: str, system_prompt: str = "You are a helpful AI") -> str:
    payload = {
        "model": LLMConfig.MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": LLMConfig.TEMPERATURE,
    }

    start = time.time()

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=LLMConfig.TIMEOUT,
    )

    duration = time.time() - start
    print(f"LLM RESPONSE TIME: {duration:.2f}s")

    if response.status_code != 200:
        raise Exception(response.text)

    result = response.json()

    # Consumo informado por la API de Groq
    usage = result.get("usage") or {}

    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get(
        "total_tokens",
        input_tokens + output_tokens,
    )

    # Calcular costo únicamente si conocemos la tarifa del modelo
    pricing = PRICING_PER_MILLION.get(LLMConfig.MODEL)

    if pricing:
        input_cost = input_tokens * pricing["input"] / 1_000_000
        output_cost = output_tokens * pricing["output"] / 1_000_000
        total_cost = input_cost + output_cost
        cost_text = f"${total_cost:.8f}"
    else:
        input_cost = None
        output_cost = None
        total_cost = None
        cost_text = "N/A (tarifa no configurada)"

    print("=" * 60)
    print("LLM USAGE")
    print(f"Request ID:    {result.get('id', 'N/A')}")
    print(f"Model:         {result.get('model', LLMConfig.MODEL)}")
    print(f"Input tokens:  {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens:  {total_tokens}")
    print(f"Input cost:    ${input_cost:.8f}" if input_cost is not None else "Input cost: N/A")
    print(f"Output cost:   ${output_cost:.8f}" if output_cost is not None else "Output cost: N/A")
    print(f"Total cost:    {cost_text}")
    print("=" * 60)

    return result["choices"][0]["message"]["content"]