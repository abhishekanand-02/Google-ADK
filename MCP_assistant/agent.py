"""
File Reader Assistant Agent

Demonstrates MCP tools integration with ADK using the filesystem MCP server.

Reference: https://google.github.io/adk-docs/tools-custom/mcp-tools/
"""

import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Allowed directory for the filesystem MCP server (next to this package).
# Name avoids ambiguous UI truncation ("my_files" → "myfile").
ALLOWED_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "allowed_files"))
os.makedirs(ALLOWED_PATH, exist_ok=True)

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="file_reader_assistant",
    description="Helps users read and explore files using MCP tools.",
    instruction="""
You are a file reader assistant that helps users explore files.

The MCP filesystem server exposes tools including:
- list_directory — list entries in a path under the allowed folder
- read_text_file — read a text file under the allowed folder

When helping users:
1. Use list_directory to show available files
2. Use read_text_file to display file contents when asked
3. Describe what you find in a helpful way

Always be clear that you only access the configured allowed directory.
""",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        ALLOWED_PATH,
                    ],
                ),
            ),
            # Official tool names from @modelcontextprotocol/server-filesystem (not read_file)
            tool_filter=["list_directory", "read_text_file"],
        ),
    ],
)
