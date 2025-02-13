from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    GradioUI,
    FinalAnswerTool,
    HfApiModel,
    ToolCallingAgent,
)
from tools.visit_webpage import visit_webpage
from tools.web_agent import (
    open_webpage, save_screenshot, search_item_ctrl_f, go_back, close_popups,
    click_element
)
import os


# HF TOKEN
token = os.getenv("HF_TOKEN")

# TOOLS
search_tool = DuckDuckGoSearchTool()
final_answer_tool = FinalAnswerTool()


# MODEL
# Inference model for the agents
model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    provider="hf-inference",
    token=token,
    timeout=120
)

# Create the agent
web_search_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), visit_webpage],
    model=model,
    name="web_search_agent",
    description="Agent to make web searches.",
)

web_agent = CodeAgent(
    tools=[
        open_webpage,
        click_element,
        go_back,
        close_popups,
        search_item_ctrl_f,
        final_answer_tool
    ],
    model=model,
    additional_authorized_imports=["helium"],
    step_callbacks=[save_screenshot],
    max_steps=50,
    name="web_agent",
    description="Agent to visit web pages and interact with them.",
)

# Import helium for the agent
web_agent.python_executor("from helium import *", web_agent.state)

# Création du manager d'agents
manager_agent = CodeAgent(
    tools=[],
    model=model,
    additional_authorized_imports=['requests', 'bs4'],
    managed_agents=[web_agent, web_search_agent],
)

GradioUI(manager_agent).launch()
