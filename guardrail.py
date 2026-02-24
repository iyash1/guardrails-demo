from datetime import datetime
from agents import Agent, RunContextWrapper, input_guardrail, GuardrailFunctionOutput, TResponseInputItem, Runner
from dataModels import PoliticalTopicOutput, DefenseTopicOutput

# ----------------------------------------------------
# Guardrails Setup
# ----------------------------------------------------
politics_guardrail_agent = Agent(
    name = "Guardrail check",
    instructions = "Check if the user is asking about political topics, politicians, elections, government policy, or anything related to politics. If so, set is_political to true and explain why in reasoning.",
    output_type = PoliticalTopicOutput
    )

defense_guardrail_agent = Agent(
    name = "Defense-related guardrail check",
    instructions = "Check if the user is asking about defense-related topics, such as military actions, defense companies, weapons, or anything related to defense. If so, set is_defense_related to true and explain why in reasoning.",
    output_type = DefenseTopicOutput
    )
# @input_guardrail: decorator that marks the function 
# The function takes:
# ctx: a wrapper object holding context/state for the current run (things like conversation history, metadata, or session info).
# input: what the user typed in (either a string, or a structured list of TResponseInputItem).
# The function returns a GuardrailFunctionOutput: what did we find, and do we trip the guardrail?

@input_guardrail
async def politics_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    
    # Use the guardrail agent to classify the input.
    result = await Runner.run(politics_guardrail_agent, input, context = ctx.context)
    if result.final_output.is_political:
        print(f"\n ⚠️ GUARDRAIL CHECK ⚠️ This is a politics-related query! {result.final_output.reasoning} \n")

    # output_info: stores the full structured output (is_political + reasoning).
    # tripwire_triggered: this is the key flag. If is_political == True, then the guardrail has been triggered.
    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_political
        )

@input_guardrail
async def defense_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:    
    result = await Runner.run(defense_guardrail_agent, input, context = ctx.context)
    if result.final_output.is_defense_related:
        print(f"\n ⚠️ GUARDRAIL CHECK ⚠️ This is a defense-related query! {result.final_output.reasoning} \n")

    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_defense_related
        )