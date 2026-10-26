from pathlib import Path


def instructions():
    return (Path(__file__).resolve().parent.parent / 'skills/travel_agent.md').read_text(encoding='utf8')
