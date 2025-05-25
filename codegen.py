import re
import requests
import json

OLLAMA_API_URL = 'http://localhost:11434/api/generate'  # Default Ollama endpoint
OLLAMA_MODEL = 'codellama'  # You can change this to your preferred code model

# Helper to call Ollama API
def call_ollama(prompt, model=OLLAMA_MODEL):
    response = requests.post(
        OLLAMA_API_URL,
        json={
            'model': model,
            'prompt': prompt,
            'stream': False
        }
    )
    response.raise_for_status()
    result = response.json()
    return result.get('response', '')

# Helper to extract function signature/parameters from code
PARAM_REGEX = re.compile(r'def main\\((.*?)\\):')

def extract_parameters(code):
    match = PARAM_REGEX.search(code)
    if match:
        params = match.group(1)
        return [p.strip() for p in params.split(',') if p.strip()]
    return []

def generate_tool_code(user_request, spec):
    # Extract a simple tool name from the request
    tool_name = re.sub(r'[^a-zA-Z0-9_]', '_', user_request.strip().lower())[:20]
    # Compose prompt for Ollama
    prompt = f"""
You are an autonomous agent that generates Python command-line tools based on user requests.
Request: {user_request}
Specification: {spec}

- The tool should be a single Python file.
- It should have a main() function as the entry point.
- If the tool needs to store data (like memos), use a local file in the same directory.
- Print output to the console.
- Only output the code, no explanations.
"""
    code = call_ollama(prompt)
    params = extract_parameters(code)
    return code, tool_name, params

if __name__ == '__main__':
    main() 