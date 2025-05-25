from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EchoServer")

@mcp.tool()
def echo_tool(message: str) -> str:
    return f"Echo: {message}"

if __name__ == "__main__":
    mcp.run() 