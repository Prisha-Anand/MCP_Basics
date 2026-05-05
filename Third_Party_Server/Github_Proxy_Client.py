import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import dotenv
from fastmcp import Client

dotenv.load_dotenv()
async def main():
    async with Client("http://localhost:8000/mcp/", auth="oauth") as client:
        await client.ping()
        tools = await client.list_tools()
        #print("Available tools:", tools)
        result = await client.call_tool(
        "search_repositories",
        {
            "query": "user:Prisha-Anand"
        }
    )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())