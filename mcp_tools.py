from functions import codebase_search, run_terminal_cmd, web_search

MCP_TOOLS = [
    {
        'name': 'codebase_search',
        'description': 'Search the codebase for relevant code snippets.',
        'function': codebase_search,
        'params': ['query', 'target_directories', 'explanation']
    },
    {
        'name': 'run_terminal_cmd',
        'description': 'Run a terminal command on the system.',
        'function': run_terminal_cmd,
        'params': ['command', 'is_background', 'explanation']
    },
    {
        'name': 'web_search',
        'description': 'Search the web for real-time information.',
        'function': web_search,
        'params': ['search_term', 'explanation']
    },
    # Add more MCP tools as needed
]

def find_mcp_tool(user_request):
    # Simple keyword match in description or name
    for tool in MCP_TOOLS:
        if any(word in tool['description'].lower() or word in tool['name'].lower() for word in user_request.lower().split()):
            return tool
    return None 