"""Gradio chat: session conversation + a concise cross-session Markdown memory."""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import gradio as gr
from harness.agent import reply

logger = logging.getLogger("travel_agent")
logger.setLevel(logging.ERROR)
if not logger.handlers:
    log_path = Path(__file__).with_name("travel_agent.log")
    handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)


def chat(message, history):
    if not message.strip():
        return "Please enter a travel question."
    if not os.environ.get("OPENAI_API_KEY"):
        return "OPENAI_API_KEY missing; add a Codespaces repository secret."
    try:
        return reply(message, history)
    except Exception as exc:
        logger.exception("Travel research failed")
        return f"Travel research failed ({type(exc).__name__}). Check travel_agent.log."


with gr.Blocks(title="Travel Service Agent") as demo:
    gr.Markdown("# Travel Service Agent\nResearch flights, hotels and rental cars. No bookings or reservation payments.")
    gr.ChatInterface(
        fn=chat,
        chatbot=gr.Chatbot(height=520),
        examples=[
            "Find round-trip flights DFW to SFO departing Nov 12, 2026 and returning Nov 16, under $450.",
            "Find hotels near Union Square in San Francisco for Nov 12–16, 2026.",
            "Find rental cars at SFO for Nov 12–16, 2026.",
        ],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
