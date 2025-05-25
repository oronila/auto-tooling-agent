# Auto Tool Agent MVP

This is a minimal agent that can generate and run its own Python tools based on user requests.

## How it works
- You type a request (e.g., "convert CSV to JSON").
- The agent checks if a tool exists for your request.
- If not, it asks for more details, generates a Python script, saves it, and runs it.
- All tools are stored in the `tools/` directory for future use.

## Project Structure
- `main.py` — Main entry point, handles user interaction.
- `tool_registry.py` — Manages tool storage and lookup.
- `codegen.py` — Generates Python code for new tools (stub for now).
- `sandbox.py` — Runs tools in a subprocess.
- `tools/` — Directory for generated tools and metadata.

## Usage
1. Ensure you have Python 3.7+ installed.
2. Run:
   ```bash
   python main.py
   ```
3. Follow the prompts to create or use tools.

## Notes
- This is an MVP. Generated tools are stubs; real codegen would use an LLM.
- No advanced sandboxing or security yet.
