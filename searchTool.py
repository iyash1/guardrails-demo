import os, requests
from dotenv import load_dotenv
from colorama import Fore, Style, init
from agents import function_tool
from dataModels import TavilyParams
from constants import TAVILY_SEARCH_URL

load_dotenv()
init(autoreset=True)

tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError(f"{Fore.RED} ➡️ TAVILY_API_KEY not found in environment variables. ❌ {Style.RESET_ALL}")
else:
    print(f""" {Fore.GREEN} ➡️ TAVILY API key loaded successfully. ✅ {Style.RESET_ALL}""")
    
@function_tool
def tavily_search(params: TavilyParams) -> str:
    url = TAVILY_SEARCH_URL
    payload = {
        "api_key": tavily_api_key,
        "query": params["query"],
        "max_results": params.get("max_results", 3),
    }
    resp = requests.post(url, json = payload, headers = {"Content-Type": "application/json"})
    if resp.status_code != 200:
        return f"{Fore.RED} 🛑 Tavily error! \n{resp}{Style.RESET_ALL}"
    items = resp.json().get("results", [])
    return "\n".join([f"- {itm['title']}: {itm['content']}" for itm in items]) or "No hits"