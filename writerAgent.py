from dataModels import FinalReport
from agents import Agent, RunResult
from fundamentalAnalysisAgent import fundamentals_agent
from searchAgent import search_agent
from constants import MAIN_MODEL

async def extract_summary(run_result: RunResult) -> str:
    # Extracts the 'summary' field from the final_output of an agent run.
    return run_result.final_output.summary

# Define the writer agent
def getWriterAgent():
    writer_agent = Agent(name = "Writer",
                        instructions = ("""Context: You are an expert research writer preparing a comprehensive investment report on a company, using diverse information sources. Your audience is sophisticated and expects clarity, depth, and actionable insights.
            Instruction: Thoroughly analyze the provided search snippets and analyst summaries. Synthesize these into a cohesive, well-structured markdown report of at least 600 words. Your report must: (1) begin with a concise 2-3 sentence executive summary capturing the most critical findings; (2) integrate and cross-reference key facts, trends, and perspectives from all sources, highlighting both consensus and disagreement; (3) organize content with clear headings and logical flow; (4) maintain objectivity, cite evidence, and avoid speculation; (5) conclude with 3-5 insightful, specific follow-up research questions that would meaningfully advance understanding or address unresolved issues. 
            Ensure the writing is precise, professional, and tailored for an investment decision-making context.
            You must always use the 'search' tool to gather and incorporate up-to-date information in your report. The other tools—'fundamentals'—are optional and should only be used if the user specifically requests those analyses or if you determine that including them would significantly enhance the report's quality or relevance.

            Input: A set of search snippets and analyst summaries containing relevant information about the company, and any user instructions specifying which analyses to include.
            Output: A markdown-formatted report (minimum 600 words) including an executive summary and 3-5 well-crafted follow-up research questions.
            Tools: The following tools are available for comprehensive research on the company:
            - fundamentals: Get fundamentals analysis (optional)
            - search: Get search results (required)
            """
        ),
        model = MAIN_MODEL,
        output_type = FinalReport,

        # Note that fundamentals_agent and search_agent are other AI agents we defined earlier.
        # The method .as_tool(...) wraps each of them into a callable tool so that the writer_agent can use them.
        # This means the writer agent is not working alone — it can “call” the search agent (required) and fundamentals agent (optional) as helper sub-agents.
            
        tools = [
            fundamentals_agent.as_tool(
                "fundamentals",
                "Get fundamentals analysis",
                custom_output_extractor = extract_summary,
            ),
            search_agent.as_tool(
                "search",
                "Get search results",
                custom_output_extractor = extract_summary,
            ),
        ],

    )
    return writer_agent