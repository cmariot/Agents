from smolagents import (
    CodeAgent, HfApiModel, load_tool, tool
)
import datetime
import pytz
import yaml
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI


# # ########################################################################### #
# #                                                                             #
# # Tool Definitions                                                            #
# #                                                                             #
# # ########################################################################### #


# # Define a tool that fetches the current time in a specified timezone

# @tool
# def get_current_time_in_timezone(timezone: str) -> str:
#     """A tool that fetches the current local time in a specified timezone.
#     Args:
#         timezone: A string representing a valid timezone
#         (e.g., 'America/New_York').
#     """
#     try:
#         # Create timezone object
#         tz = pytz.timezone(timezone)
#         # Get current time in that timezone
#         local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
#         return f"The current local time in {timezone} is: {local_time}"
#     except Exception as e:
#         return f"Error fetching time for timezone '{timezone}': {str(e)}"


# # Import a tool from the tools directory

# final_answer = FinalAnswerTool()


# # Import tool from Hub

# image_generation_tool = load_tool(
#     "agents-course/text-to-image", trust_remote_code=True
# )


# ########################################################################### #
#                                                                             #
# Model                                                                       #
#                                                                             #
# ########################################################################### #


model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)


# ########################################################################### #
#                                                                             #
# Agent                                                                       #
#                                                                             #
# ########################################################################### #


with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[
        image_generation_tool,
        get_current_time_in_timezone,
        final_answer
    ],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


manager_agent = CodeAgent(
    tools=[],
    model=model,
    additional_authorized_imports=['requests', 'bs4'],
    managed_agents=[web_agent, web_search_agent],
)

# ########################################################################### #
#                                                                             #
# Gradio UI                                                                   #
#                                                                             #
# ########################################################################### #


GradioUI(agent).launch()
