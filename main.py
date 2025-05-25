import os
import asyncio
from tool_registry import ToolRegistry
from codegen import generate_tool_code
from sandbox import run_tool_sandboxed
from mcp_tools import find_mcp_tool
from mcp_client import MCPClientWrapper

TOOLS_DIR = 'tools'

async def main():
    os.makedirs(TOOLS_DIR, exist_ok=True)
    registry = ToolRegistry(TOOLS_DIR)
    print("Welcome to the Auto Tool Agent! Type 'exit' to quit.")

    # Optionally connect to an MCP server (adjust command/args as needed)
    mcp_client = MCPClientWrapper(server_command="python", server_args=["echo_server.py"])
    await mcp_client.connect()
    mcp_tools = await mcp_client.list_tools()
    mcp_tool_names = [tool.name for tool in mcp_tools]

    while True:
        user_input = input("\nWhat do you want to do? ")
        if user_input.strip().lower() == 'exit':
            break
        # Check for MCP tool match first
        # Try to match by tool name
        matched_tool = None
        for tool in mcp_tools:
            if tool.name in user_input or tool.description and tool.description.lower() in user_input.lower():
                matched_tool = tool
                break
        if matched_tool:
            print(f"Using MCP tool: {matched_tool.name}")
            params = {}
            for arg in matched_tool.arguments:
                value = input(f"Enter value for '{arg.name}': ")
                params[arg.name] = value
            try:
                result = await mcp_client.call_tool(matched_tool.name, params)
                print(f"Result:\n{result}")
            except Exception as e:
                print(f"Error running MCP tool: {e}")
            continue
        # Otherwise, check for local MCP tool (legacy)
        mcp_tool = find_mcp_tool(user_input)
        if mcp_tool:
            print(f"Using MCP tool: {mcp_tool['name']}")
            params = {}
            for param in mcp_tool['params']:
                value = input(f"Enter value for '{param}': ")
                params[param] = value
            try:
                result = mcp_tool['function'](**params)
                print(f"Result:\n{result}")
            except Exception as e:
                print(f"Error running MCP tool: {e}")
            continue
        # Otherwise, check for custom tool
        tool = registry.find_tool(user_input)
        if tool:
            print(f"Running existing tool: {tool['name']}")
            result = run_tool_sandboxed(tool['path'])
            print(f"Result:\n{result}")
        else:
            print("No tool found. Let's create one!")
            spec = input("Describe the input/output and any details for this tool: ")
            code, tool_name, params = generate_tool_code(user_input, spec)
            tool_path = registry.save_tool(tool_name, code, user_input, params)
            print(f"Generated tool '{tool_name}'. Running it now...")
            result = run_tool_sandboxed(tool_path)
            print(f"Result:\n{result}")

if __name__ == "__main__":
    asyncio.run(main()) 