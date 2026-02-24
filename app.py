import os, asyncio
from colorama import Fore, Style, init
from dotenv import load_dotenv
from agents import Runner
from agents import Runner


# -------------------------------------------------------------------
# Initialization and API Key Loading
# -------------------------------------------------------------------
print(f"{Fore.MAGENTA} 🏃‍♂️‍➡️ Loading environment variables...{Style.RESET_ALL}\n")
load_dotenv()
init(autoreset=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError(f"{Fore.RED} ➡️ OPENAI_API_KEY not found in environment variables. ❌ {Style.RESET_ALL}")
else:
    print(f""" {Fore.GREEN} ➡️ OPENAI API key loaded successfully. ✅ {Style.RESET_ALL}""")

# -------------------------------------------------------------------
# Load the agents 
# -------------------------------------------------------------------
from plannerAgent import getPlannerAgent
planner_agent = getPlannerAgent()

from handoff import handoff_from_planner_to_writer

# ---------------------------------------------------
# Main Execution Loop
# ---------------------------------------------------
async def main(user_input):
    try:
        # Trip's guardrail --> "Why is Trump meeting with Putin this week?"
        # Doesn't trip guardrail --> "solid state battery companies"
        run = await Runner.run(starting_agent = planner_agent, input = user_input)
        await handoff_from_planner_to_writer(user_input)  # This will print the user query and the final report from Writer
        # print(f"---\n### 🤖 Agent’s Answer\n{run.final_output}\n---")
    except Exception as e:
        print(f"{Fore.RED} 🛑 Error during main execution: {e}{Style.RESET_ALL}\n")

# ---------------------------------------------------
# Command-line Interface
# ---------------------------------------------------
if __name__ == "__main__":
    try:
        while True:
            user_input = input(f"{Fore.YELLOW}Enter your research request (or 'exit' to quit): {Style.RESET_ALL}")
            if user_input.lower() == "exit":
                print(f"{Fore.MAGENTA}👋🏻 Exiting. Goodbye!{Style.RESET_ALL}\n")
                break

            if not user_input.strip():
                print(f"{Fore.RED}⚠️ Please enter a valid research request.{Style.RESET_ALL}\n")
                continue

            asyncio.run(main(user_input))
    except (KeyboardInterrupt, ValueError, Exception) as e:
        print(f"{Fore.RED} 🛑 ERROR: \n {e}{Style.RESET_ALL}\n")