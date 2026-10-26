"""Durable markdown memory; Gradio supplies in-session conversation history."""
from pathlib import Path
from datetime import datetime, timezone
from threading import Lock
import json
import os

MEMORY_PATH = Path(os.getenv("TRAVEL_MEMORY_FILE", "memory/travel_memory.md"))
_LOCK = Lock()


def read_memory():
    if not MEMORY_PATH.exists():
        return "No saved traveler preferences."
    return MEMORY_PATH.read_text(encoding="utf-8")[:12000]


def update_memory(client, model, user_message):
    """Add only durable user-stated preferences or explicit changes, never full transcripts.

    This is a simple teaching example for a single-user Codespace, not a
    secure multiuser store. LLM-extracted facts should be reviewed by the user.
    """
    current = read_memory()
    response = client.responses.create(
        model=model,
        instructions=(
            "Extract durable travel preferences or facts the USER explicitly stated in "
            "the latest message. Return JSON ONLY as {\"facts\": [\"...\"]}. "
            "Examples: preferred airports, airline preferences, accessibility needs if "
            "explicitly requested for future use, permanent budgets. A stated trip "
            "plan may be saved if clearly confirmed, including dates. "
            "Do NOT save a search question, guesses, temporary exploration, "
            "full conversation, payment data, account identifiers, addresses, "
            "passport details, medical information, or secrets. "
            "If nothing durable was stated, return an empty list. "
            "If the user changes a preference, output its new value; avoid duplicates."
        ),
        input=[{"role": "user", "content": "Existing memory:\n" + current +
                "\n\nLatest user message:\n" + user_message}],
    )
    try:
        facts = json.loads(response.output_text or "{}").get("facts", [])
    except (ValueError, TypeError):
        return
    if not isinstance(facts, list):
        return
    clean = []
    for fact in facts[:8]:
        if isinstance(fact, str):
            fact = " ".join(fact.strip().split())[:300]
            if fact and len(fact) > 3:
                clean.append(fact)
    if not clean:
        return
    with _LOCK:
        MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not MEMORY_PATH.exists():
            MEMORY_PATH.write_text("# Travel Agent Memory\n\n## Durable preferences and confirmed plans\n", encoding="utf-8")
        existing = MEMORY_PATH.read_text(encoding="utf-8")
        seen = {line.removeprefix("- ").strip().casefold() for line in existing.splitlines()}
        new = [fact for fact in clean if fact.casefold() not in seen]
        if new:
            with MEMORY_PATH.open("a", encoding="utf-8") as f:
                for fact in new:
                    f.write("- " + fact + "\n")
