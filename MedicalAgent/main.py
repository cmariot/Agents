# Assistant médical pour les professionnels :
# Un agent qui aide les médecins à remplir les dossiers patients,
# rédiger des comptes-rendus et proposer des diagnostics différenciels basés
# sur des guidelines médicales.
# Optimise les tâches administratives et de recherche d'informations.


# Import the necessary tools
from smolagents.models import HfApiModel
from smolagents import CodeAgent
from smolagents import GradioUI
from tools.api_call import ApiCallTool
from tools.final_answer import FinalAnswerTool
import os
from prompts import rag_template_prompt, web_agent_prompt, main_agent_prompt


# HF TOKEN
token = os.getenv("HF_TOKEN")

# ########################################################################### #
#                                                                             #
# Model                                                                       #
#                                                                             #
# ########################################################################### #

# Define the model
model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    provider="hf-inference",
    token=token,
    timeout=120
)


# ########################################################################### #
#                                                                             #
# Web Agent                                                                   #
#                                                                             #
# ########################################################################### #

# Define the web_agent
web_agent = CodeAgent(
    model=model,
    tools=[
        ApiCallTool(),
        FinalAnswerTool(),
    ],

    max_steps=3,
    verbosity_level=2,
    grammar=None,
    planning_interval=None,
    prompt_templates=web_agent_prompt,
    name="Web Agent",
    description="""
    An agent that can make API calls and generate final answers.

    Args:
        method (str): The HTTP method to use for the API call.
        url (str): The URL to make the API call to.
        headers (dict): The headers to include in the API call.
        More options in the kwargs
    Returns:
        The response from the API call.
    Example:
        response = web_agent("GET", "https://api.example.com/data", headers={"Authorization": "Bearer token"})
    """,
    # prompt_templates=None,
    additional_authorized_imports=[
        "requests"
    ]

)

# ########################################################################### #
#                                                                             #
# RAG Agent                                                                   #
#                                                                             #
# ########################################################################### #

# Define the rag_agent
rag_agent = CodeAgent(
    model=model,
    tools=[
        FinalAnswerTool()
    ],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="RAG Agent",
    description="An agent that retrieves and generates medical data.",
    prompt_templates=rag_template_prompt,
)


# ########################################################################### #
#                                                                             #
# Main Agent                                                                  #
#                                                                             #
# ########################################################################### #

# Define the main agent
agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[
        web_agent,
        rag_agent
    ],
    additional_authorized_imports=["time", "requests"],
    name="Main Agent",
    description="""
    An agent that can make API calls and generate final answers.
    Calls the Web Agent to process medical data and generate a final answer.

    Args:
        method (str): The HTTP method to use for the API call.
        url (str): The URL to make the API call to.
        headers (dict): The headers to include in the API call.
        More options in the kwargs
    Returns:
        The response from the API call.
    Example:
        response = agent("GET", "https://api.example.com/data", headers={"Authorization": "Bearer token"})
    """,
    prompt_templates=main_agent_prompt
)


# agent.launch()
# Assistant médical pour les professionnels :
# Un agent qui aide les médecins à remplir les dossiers patients,
# rédiger des comptes-rendus et proposer des diagnostics différenciels basés
# sur des guidelines médicales.
# Optimise les tâches administratives et de recherche d'informations.

# On peux ajouter des outils ici pour améliorer les fonctionnalités.
prompt = "Traiter les données médicales"

# Ajouter un RAG pour avoir des réponses plus précises.
# RAG : Retrieve and Generate
# RAG est un modèle qui combine un modèle de recherche (Retrieve) et un modèle de génération (Generate).
# Le modèle de recherche est utilisé pour trouver des informations pertinentes sur le Web,
# On peut utiliser des API


# def integrate_rag_model(agent, query):
#    # Use the RAG model to generate a response

# response = integrate_rag_model(agent, prompt)

# Generate a response
# response = agent(prompt)

# # Print the response
# print(response)

# Stocker les résultats dans une db pour une récupération rapide (RAG).

# ########################################################################### #
#                                                                             #
# Here is the final answer from your managed agent 'Main Agent':              #
#                                                                             #
# ########################################################################### #

# Here is the final answer from your managed agent 'Main Agent':

# ### 1. Task outcome (short version):
# Processed medical data through systematic collection, cleaning, transformation, analysis, security, storage, sharing, and interpretation.

# ### 2. Task outcome (extremely detailed version):
# #### Data Collection:
# - Ensure systematic and ethical data collection.
# - Respect patient confidentiality.
# - Comply with relevant regulations (e. g., HIPAA in the U. S.).

# #### Data Cleaning:
# - Handle missing values (e. g., imputation, removal).
# - Remove duplicates.
# - Correct errors.
# - Ensure data consistency.

# #### Data Transformation:
# - Normalize data formats.
# - Standardize units.
# - Encode categorical variables.
# - Aggregate data if necessary.

# #### Data Analysis:
# - Perform statistical analysis.
# - Identify trends.
# - Extract insights using appropriate techniques (e. g., regression analysis, clustering).

# #### Data Security:
# - Implement robust security measures.
# - Use encryption.
# - Manage access controls.
# - Conduct regular audits.

# #### Data Storage:
# - Use secure and scalable storage solutions.
# - Consider Electronic Health Records (EHR) systems.

# #### Data Sharing:
# - Establish protocols for sharing data.
# - Ensure compliance with data sharing regulations (e. g., Common Rule, GDPR).

# #### Data Interpretation:
# - Ensure correct interpretation of data.
# - Avoid misinterpretation that could lead to incorrect conclusions.

# ### 3. Additional context (if relevant):
# - Medical data processing is crucial for improving healthcare outcomes.
# - Data should be handled with the utmost care to protect patient privacy.
# - Continuous monitoring and updates are necessary to adapt to changing regulatory requirements.


# ########################################################################### #
#                                                                             #
# Gradio UI                                                                   #
#                                                                             #
# ########################################################################### #


GradioUI(agent=agent).launch()

# Connect this to a cms if your goal is to centralize your business data with a chatbot, then using this data as context.
