import ollama


class Agent:

    def __init__(
        self,
        model: str = "mistral-large",
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

