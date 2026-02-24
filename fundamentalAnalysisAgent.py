from searchTool import tavily_search
from agents import Agent
from dataModels import Summary
from constants import MAIN_MODEL

fundamentals_agent = Agent(
    name = "FundamentalsAnalyst",
    instructions = """
    Context: You are a financial analyst specializing in company fundamentals.
    Instruction: Carefully analyze the provided notes to assess the company's financial fundamentals, including revenue, growth, and margins.
    Input: Notes containing relevant financial data and qualitative information about the company.
    Output: A concise summary (≤200 words) highlighting key points about the company's revenue, growth trajectory, and profit margins.
    Tools: The following tools are available for comprehensive research on the company:
    - tavily_search: Search the web for information about the company.
    """,
    output_type = Summary,
    model = MAIN_MODEL,
    tools = [tavily_search])