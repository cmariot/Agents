from smolagents import CodeAgent, DuckDuckGoSearchTool, GradioUI, FinalAnswerTool, Model, ChatMessage, Tool
from smolagents.models import parse_tool_args_if_needed
from huggingface_hub import InferenceClient

# from dotenv import load_dotenv
# import ollama
# from dataclasses import dataclass

# Charger les variables d'environnement
# load_dotenv()


# @dataclass
# class Message:
#     content: str  # Attribut requis pour smolagents


# class OllamaModel:
#     def __init__(self, model_name):
#         self.model_name = model_name
#         self.client = ollama.Client()

#     def __call__(self, messages, **kwargs):
#         formatted_messages = []

#         # S'assurer que les messages sont correctement formatés
#         for msg in messages:
#             if isinstance(msg, str):
#                 formatted_messages.append({
#                     "role": "user",
#                     "content": msg
#                 })
#             elif isinstance(msg, dict):
#                 role = msg.get("role", "user")
#                 content = msg.get("content", "")
#                 if isinstance(content, list):
#                     content = " ".join(
#                         part.get("text", "") for part in content
#                         if isinstance(part, dict) and "text" in part
#                     )
#                 formatted_messages.append({
#                     "role": role if role in [
#                         'user', 'assistant', 'system', 'tool'] else 'user',
#                     "content": content
#                 })
#             else:
#                 formatted_messages.append({
#                     "role": "user",
#                     "content": str(msg)
#                 })

#         response = self.client.chat(
#             model=self.model_name,
#             messages=formatted_messages,
#             options={'temperature': 0.7, 'stream': False}
#         )

#         # Renvoyer un objet Message avec l'attribut 'content'
#         return Message(
#             content=response.get("message", {}).get("content", "")
#         )


from typing import List, Optional, Dict
import os


class HfApiModel(Model):
    """A class to interact with Hugging Face's Inference API for language model interaction.

    This model allows you to communicate with Hugging Face's models using the Inference API. It can be used in both serverless mode or with a dedicated endpoint, supporting features like stop sequences and grammar customization.

    Parameters:
        model_id (`str`, *optional*, defaults to `"Qwen/Qwen2.5-Coder-32B-Instruct"`):
            The Hugging Face model ID to be used for inference. This can be a path or model identifier from the Hugging Face model hub.
        provider (`str`, *optional*):
            Name of the provider to use for inference. Can be `"replicate"`, `"together"`, `"fal-ai"`, `"sambanova"` or `"hf-inference"`.
            defaults to hf-inference (HF Inference API).
        token (`str`, *optional*):
            Token used by the Hugging Face API for authentication. This token need to be authorized 'Make calls to the serverless Inference API'.
            If the model is gated (like Llama-3 models), the token also needs 'Read access to contents of all public gated repos you can access'.
            If not provided, the class will try to use environment variable 'HF_TOKEN', else use the token stored in the Hugging Face CLI configuration.
        timeout (`int`, *optional*, defaults to 120):
            Timeout for the API request, in seconds.
        custom_role_conversions (`dict[str, str]`, *optional*):
            Custom role conversion mapping to convert message roles in others.
            Useful for specific models that do not support specific message roles like "system".
        **kwargs:
            Additional keyword arguments to pass to the Hugging Face API.

    Raises:
        ValueError:
            If the model name is not provided.

    Example:
    ```python
    >>> engine = HfApiModel(
    ...     model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    ...     token="your_hf_token_here",
    ...     max_tokens=5000,
    ... )
    >>> messages = [{"role": "user", "content": "Explain quantum mechanics in simple terms."}]
    >>> response = engine(messages, stop_sequences=["END"])
    >>> print(response)
    "Quantum mechanics is the branch of physics that studies..."
    ```
    """

    def __init__(
        self,
        model_id: str = "Qwen/Qwen2.5-Coder-32B-Instruct",
        provider: Optional[str] = None,
        token: Optional[str] = None,
        timeout: Optional[int] = 120,
        custom_role_conversions: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.provider = provider
        if token is None:
            token = os.getenv("HF_TOKEN")
        self.client = InferenceClient(self.model_id, provider=provider, token=token, timeout=timeout)
        self.custom_role_conversions = custom_role_conversions

    def __call__(
        self,
        messages: List[Dict[str, str]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        **kwargs,
    ) -> ChatMessage:
        completion_kwargs = self._prepare_completion_kwargs(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            convert_images_to_image_urls=True,
            custom_role_conversions=self.custom_role_conversions,
            **kwargs,
        )
        response = self.client.chat_completion(**completion_kwargs)

        self.last_input_token_count = response.usage.prompt_tokens
        self.last_output_token_count = response.usage.completion_tokens
        message = ChatMessage.from_hf_api(response.choices[0].message, raw=response)
        if tools_to_call_from is not None:
            return parse_tool_args_if_needed(message)
        return message


# from smolagents import CodeAgent, LiteLLMModel

# model = LiteLLMModel(
#     model_id="ollama_chat/llama3.2", # This model is a bit weak for agentic behaviours though
#     api_base="http://localhost:11434", # replace with 127.0.0.1:11434 or remote open-ai compatible server if necessary
#     api_key="YOUR_API_KEY" # replace with API key if necessary
#     num_ctx=8192 # ollama default is 2048 which will fail horribly. 8192 works for easy tasks, more is better. Check https://huggingface.co/spaces/NyxKrage/LLM-Model-VRAM-Calculator to calculate how much VRAM this will need for the selected model.
# )

# Définition des outils
# image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)
search_tool = DuckDuckGoSearchTool()
final_answer_tool = FinalAnswerTool()

# Définition du modèle Ollama personnalisé
# ollama_model = OllamaModel("mistral:latest")

# Création de l'agent
agent = CodeAgent(
    tools=[search_tool, final_answer_tool],
    model=HfApiModel(),
    # model=ollama_model,
    additional_authorized_imports=['requests', 'bs4'],
    planning_interval=3
)

# Exécution de l'agent
# result = agent.run(
#     "Quel temps fait il actuellement à Paris ?"
# )

# Affichage du résultat
# print(result)

GradioUI(agent).launch()

