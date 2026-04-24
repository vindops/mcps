# Weather MCP Server

A simple MCP server that provides weather forecasts using the AccuWeather API.

## Setup

```bash
# Install uv: https://docs.astral.sh/uv/getting-started/installation/

uv venv
uv sync
```

## Run the MCP server locally
```bash
cp env.template .env
# edit .env file

uv run main.py

npx -y @modelcontextprotocol/inspector

In the inspector UI, connect to http://localhost:8000/mcp
```
