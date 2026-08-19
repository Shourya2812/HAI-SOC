"""
rag/test_llm.py

Basic Ollama connectivity test.
"""

from rag.llm import generate_response


if __name__ == "__main__":

    prompt = """
You are a healthcare SOC analyst.

Analyze the following security event:

A PACS user exported 158 patient records.
The export occurred during an unusual hour.
There were 2 failed attempts before the successful export.
The anomaly detector assigned a score of 0.999.

Provide exactly three concise observations.

Do not invent facts that are not present in the event.
"""

    response = generate_response(prompt)

    print("\n=== Ollama Response ===\n")
    print(response)