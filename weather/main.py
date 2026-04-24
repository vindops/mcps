from mcp.server.fastmcp import FastMCP
from server import get_daily_weather
from dotenv import load_dotenv
import os

load_dotenv()

# Set MCP transport protocol. Default to stdio
# Available: 'stdio', 'streamable-http', 'sse'
MCP_TRANSPORT = os.getenv('MCP_TRANSPORT', 'stdio')

mcp = FastMCP('weather')


@mcp.tool()
async def get_daily_weather_tool(location: str, days: int = 5):
  return await get_daily_weather(location, days)


if __name__ == '__main__':
  mcp.run(transport=MCP_TRANSPORT)
