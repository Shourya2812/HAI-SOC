"""
rag/llm.py

Local LLM interface for HAI-SOC using Ollama.
"""

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:7b"


def generate_response(
    prompt: str,
    temperature: float = 0.1,
    num_predict: int = 1800,
    top_p: float = 0.9,
    timeout: int = 180,
) -> str:
    """
    Generate a concise evidence-grounded response
    using the local Ollama model.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "top_p": top_p,
        },
    }

    print(f"# Calling Ollama model: {OLLAMA_MODEL}")

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()

        if "response" not in data:
            raise ValueError(
                f"Malformed Ollama API response: missing 'response' key. Keys: {list(data.keys())}"
            )

        return data["response"].strip()

    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Failed to connect to Ollama at {OLLAMA_URL}. Is Ollama service running?")
        raise RuntimeError(f"Ollama connection error: {e}") from e
    except requests.exceptions.Timeout as e:
        print(f"[ERROR] Ollama request timed out after {timeout} seconds.")
        raise RuntimeError(f"Ollama request timeout: {e}") from e
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Ollama returned HTTP error: {e}")
        raise RuntimeError(f"Ollama HTTP error: {e}") from e
    except Exception as e:
        print(f"[ERROR] Ollama generation failed: {e}")
        raise