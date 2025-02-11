import ollama


class Agent:

    def __init__(
        self,
        model: str = "mistral-large:123b",
        memory_limit: int = 20
    ):

        """
            Agent constructor
            args:
                - model (str): Model to use for the agent
                - memory_limit (int): Number of previous messages to remember
        """

        self.model = model
        self.history = []
        self.memory_limit = memory_limit

    def _system_message(self) -> str:

        """
            Return a system message used by the agent
        """

        return """
You are an AI assistant designed to help users efficiently and accurately.
Your primary goal is to provide helpful, precise, and clear responses.

## Reasoning Process

You should follow a structured reasoning process to achieve the objective:

1. Thought: Reflect on the current situation and determine the best appro
    Use the format:
   - `Thought: {your_thought}`

2. Action (if necessary): If a tool is required, call it using the appropriate
   parameters in Python function format:
   - `Action: {your_action}`

3. Observation: Analyze the tool's output and adjust your approach if needed:
   - `Observation: {your_observation}`

Repeat this process until the objective is achieved.

## Tool Usage

You currently have access to the following tools:
- *No tools are available yet.*

## Response to the User

Once the objective is achieved, provide a direct and clear response to the user
Avoid unnecessary information and focus on delivering the best possible answer.

Keep your responses structured, logical, and easy to understand.
"""

    def ask(self, prompt: str) -> str:

        """
            Ask the agent a question
            args:
                - prompt (str): User input
            prints:
                - response_text (str): Agent response
            returns:
                - response_text (str): Agent response
        """

        self.history.append({"role": "user", "content": prompt})

        stream = ollama.chat(
            model=self.model,
            messages=self.history,
            stream=True
        )

        response_text = ""
        for chunk in stream:
            content = chunk.get("message", {}).get("content", "")
            print(content, end="", flush=True)  # Affichage progressif
            response_text += content
        print()

        self.history.append({"role": "assistant", "content": response_text})

        if len(self.history) > self.memory_limit * 2:
            self.history = self.history[-self.memory_limit * 2:]

        return response_text


# Thoughts / Actions / Observations
# ->
# Introduction / Material and Methods / Results / Discussion / Conclusion
# ?

# Introduction : Reflect on the current situation and determine the best
#                approach

# Material and Methods : If a tool is required, call it using the appropriate
#                        parameters in Python function format

# Results : Analyze the tool's output and adjust your approach if needed

# Discussion : Repeat this process until the objective is achieved

# Conclusion : Provide a direct and clear response to the user
