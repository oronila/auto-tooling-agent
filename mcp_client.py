from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

class MCPClientWrapper:
    def __init__(self, server_command, server_args=None):
        self.server_params = StdioServerParameters(command=server_command, args=server_args or [])
        self.session = None
        self.read = None
        self.write = None

    async def connect(self):
        self.read, self.write = await stdio_client(self.server_params)
        self.session = ClientSession(self.read, self.write)
        await self.session.initialize()

    async def list_tools(self):
        return await self.session.list_tools()

    async def call_tool(self, tool_name, arguments):
        return await self.session.call_tool(tool_name, arguments) 