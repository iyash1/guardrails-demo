from colorama import Fore, Style, init
from dataModels import PlannerToWriterInput
from constants import SESSION_NAME
from agents import handoff, RunContextWrapper, Runner, SQLiteSession
from writerAgent import getWriterAgent
from plannerAgent import getPlannerAgent
from agents.extensions import handoff_filters
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

init(autoreset=True)
# ---------------------------------------------------
# Initialize the SQLite session for agent handoff state management
# ---------------------------------------------------
session = SQLiteSession(SESSION_NAME)

# Callback function that runs when Planner hands off to Writer
def on_planner_to_writer(ctx: RunContextWrapper[None], input_data: PlannerToWriterInput):
    print(f" {Fore.MAGENTA}🤝 Research Complete! Intiating hand-off... Planner ➡️ Writer{Style.RESET_ALL}")  # Print a message indicating the handoff took place

# ------------------------------------------------
# Import Agents
# ------------------------------------------------
writer_agent = getWriterAgent()
planner_agent = getPlannerAgent()

# Define the actual handoff setup from Planner to Writer

handoff_to_writer = handoff(
    agent = writer_agent,                  # The target agent (Writer) that will receive the handoff
    input_type = PlannerToWriterInput,     # The type of input data expected by the Writer
    on_handoff = on_planner_to_writer,     # The callback triggered during handoff (prints the transfer message)
    tool_name_override = "transfer_to_writer",       # Custom tool name for the handoff
    tool_description_override = "Transfer to Writer with original query and search plan")  # Tool description


# Clone the Planner agent and add handoff instructions + the handoff tool
# This ensures the Planner knows how to call the Writer once the search plan is ready.
planner_with_handoff = planner_agent.clone(
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}\n\n"""
    + planner_agent.instructions
    + "\n\nWhen you have produced the SearchPlan, call the handoff tool `handoff_to_writer` with this JSON input: {{ original_query: <the user query>, search_plan: <the SearchPlan JSON> }}.\n",
    handoffs=[handoff_to_writer])  # Add the handoff to Writer

async def handoff_from_planner_to_writer(user_query: str):
    print(f"{Fore.MAGENTA}---\n## 🕵️‍♀️ User Query\n{user_query}\n---{Style.RESET_ALL}")  # Display the user query

    # Start the chain at the Planner; it will handoff to Writer
    run_res = await Runner.run(planner_with_handoff, user_query, session = session)

    # Check if the final output is from the Verifier and display the result
    report = run_res.final_output

    # Display (This part is correct)
    print("---")
    print(f"### 🔎 Executive Summary\n{report.short_summary}")
    print("-----------------\n")
    print(f"### 📄 Full Report\n{report.markdown_report}")
    print("-----------------\n")
    return run_res