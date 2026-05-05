#can use proxyProvider and link it to GitHub's MCP Server when you want to expose external tool as a part of multiple servers which you are mounting
#or use inbuilt GithubProvider if you want it to handle OAuth for eg: if prod Server - you have to use proxy if you want to access tools anyways, githubprovider only gives you auth


#ok, got it, githubProvider + Proxy Server if you want additional func on top of usual gh stuff eg: logging,auth,user details
#or if you want to aggregate multiple MCP servers(stdio/HTTP), then use Proxy
# normal gh experimentation on local then use Github Client directly



from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv()

import os
async def main():
  
    client = MultiServerMCPClient( 
        {
            "github" : {
                "command" : "npx",
                "args": ["@modelcontextprotocol/server-github"],
                "transport" : "stdio",
                "env":{
                    "GITHUB_PERSONAL_ACCESS_TOKEN" : os.getenv("GITHUB_PAT_TOKEN")
                }
            }
        }
    )
    tools = await client.get_tools()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    model = ChatGroq(model="openai/gpt-oss-120b")
    agent = create_react_agent(model=model, tools=tools)

    response = await agent.ainvoke({"messages":[{"role": "user", "content": "List all public repos for the user Prisha-Anand"}]})
    print(response['messages'][-1].content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())