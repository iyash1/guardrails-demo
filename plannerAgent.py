from datetime import datetime
from constants import MAIN_MODEL
from dataModels import SearchPlan
from guardrail import politics_guardrail, defense_guardrail
from agents import Agent

def getPlannerAgent():
    # Get today's date in YYYY-MM-DD format
    date = datetime.now().strftime("%Y-%m-%d")

    # Create an AI agent called "Planner"
    planner_agent = Agent(name = "Planner",
                          instructions = f"""Current date: {date} \n Context: You are a research planner agent tasked with designing a comprehensive research plan for a user request. 
            You have access to web search tools and should utilize the current date ({date}) when planning. 
            Instruction: Break down the user's request into 3 distinct web searches, each with a clear reason and a specific query. 
            Ensure coverage of recent news, company fundamentals, risks, sentiment, and broader context. 
            Input: The user's research request and the current date. 
            Output: A list of search plan items, each with a 'reason' and a 'query', formatted as a JSON object matching the SearchPlan schema.""",
        model = MAIN_MODEL,
        output_type = SearchPlan,
        input_guardrails = [politics_guardrail, defense_guardrail]) # THIS IS THE GUARDRAIL THAT PREVENTS POLITICAL AND DEFENSE-RELATED TOPIC ASKS
    
    return planner_agent