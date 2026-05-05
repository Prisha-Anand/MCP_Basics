import os
from fastmcp import FastMCP
from fastmcp.server import create_proxy
from fastmcp.server.auth.providers.github import GitHubProvider
from fastmcp.server.middleware.logging import LoggingMiddleware
from dotenv import load_dotenv
import logging


file_logger = logging.getLogger("github_proxy")
file_logger.setLevel(logging.INFO)
handler = logging.FileHandler("proxy.log")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
file_logger.addHandler(handler)


load_dotenv()
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

config = {
    "mcpServers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PAT_TOKEN", "")},
        }
    }
}
proxy = create_proxy(config, name="GitHub_Proxy")


proxy.auth = GitHubProvider(
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    base_url="http://localhost:8000",
)


class CustomLoggingMiddleware(LoggingMiddleware):
    async def on_call_tool(self, context, call_next):
        print(f"\n========== TOOL CALL ==========")
        print(f"Tool: {context.message.name}")
        print(f"Args: {context.message.arguments}")
        try:
            result = await call_next(context)
            print(f"---------- RESPONSE ----------\n{result}\n================================")
            return result
        except Exception as e:
            print(f"!!! ERROR in {context.message.name}: {e} !!!")
            raise

proxy.add_middleware(CustomLoggingMiddleware(
    logger=file_logger,
    include_payloads=True,
    max_payload_length=1000,
))

if __name__ == "__main__":
    proxy.run(transport="http", host="0.0.0.0", port=8000)