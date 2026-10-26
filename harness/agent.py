"""Orchestrate travel research. Session history is owned by Gradio."""
import os
from openai import OpenAI
from harness.flights import criteria_for, flight_loop
from harness.memory import read_memory, update_memory
from harness.web_search import search


def _text_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = [
            part if isinstance(part, str) else part["text"]
            for part in content
            if isinstance(part, str)
            or (isinstance(part, dict) and isinstance(part.get("text"), str))
        ]
        return "\n".join(text_parts)
    return None


def reply(message, history):
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-5.5")
    clean_history = []
    for item in history or []:
        if not isinstance(item, dict) or item.get("role") not in {"user", "assistant"}:
            continue
        content = _text_content(item.get("content"))
        if content is not None:
            clean_history.append({"role": item["role"], "content": content})
    history = clean_history
    memory = read_memory()
    criteria = criteria_for(client, model, message, history, memory)
    if criteria.get("flight_intent"):
        answer = flight_loop(client, model, criteria, history, memory)
    else:
        answer = search(client, model,
                        "Respond to the latest travel-service question (flights, hotels, cars, planning): " + message,
                        history, memory)
    # Update memory only after a successful assistant answer; failures do not block chat.
    try:
        update_memory(client, model, message)
    except Exception:
        pass
    return answer
