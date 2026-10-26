# Travel Service Agent 

## To run
Run `python app.py`

## Deployment portability
The application reads `OPENAI_API_KEY`, `OPENAI_MODEL`, and `TRAVEL_MEMORY_FILE` from process environment variables with `os.environ`/`os.getenv`, not from `devcontainer.json` or a `.env` file. 

## Repository layout
```
.devcontainer/devcontainer.json  Codespaces environment setup
app.py                          Gradio UI / within-session history
harness/agent.py                Main orchestration
harness/memory.py               Read/update memory/travel_memory.md (no database)
harness/instructions.py         Loads agent instructions from Markdown
harness/web_search.py           Responses API web search
harness/flights.py              Criteria extraction; up to five web attempts
memory/travel_memory.md         Persistent concise travel facts
skills/travel_agent.md          Agent role, safety and travel skills instructions
payments/wallet/README.md       Future Ethereum wallet slot (no implementation)
payments/mcp/sandboxes.py       Inactive Stripe/PayPal/Square sandbox stubs
requirements.txt                Latest compatible Gradio/OpenAI
```

## Search behavior and limits
A budgeted flight request triggers up to **five** web research attempts, stopping if the model reports a candidate meeting the restrictions. Without a budget, it makes one attempt. This is *not* live inventory verification and does not book travel. Hotels and car rentals use web search. Payment and Ethereum keystore components remain disabled placeholders.