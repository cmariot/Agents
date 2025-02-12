import ollama

from prompt import system_prompt
from utils.colors import CYAN, RESET, GREEN, RED


def print_color(color, text):
    print(color + text + RESET)


class Agent:
    def __init__(
        self,
        model: str = "mistral",
        memory_limit: int = 20,
        tools: list = []
    ):
        """
        Agent constructor
        args:
            - model (str): Model to use for the agent
            - memory_limit (int): Number of previous messages to remember
        """
        self.model = model
        self.memory_limit = memory_limit
        self.history = []
        self.tools = {tool.name: tool for tool in tools}

    def _system_message(self) -> str:
        """
        Return a system message used by the agent, including available tools.
        """

        tools_str = [tool.to_string() for tool in self.tools.values()]

        tool_list = "[AVAILABLE_TOOLS][" + \
            "\n- ".join(tools_str) + \
            "][/AVAILABLE_TOOLS]"

        print("Available tools:", tool_list)

        return system_prompt.format(tool_list=tool_list)

    def _call_tool(self, action: str):
        """
        Parse and execute a tool action.
        args:
            - action (str): Tool invocation string
            (e.g., 'Action: tool_name({"param": "value"})').
        returns:
            - str: The tool's output.
        """

        print(f"{GREEN}Executing tool: {action}{RESET}")

        if not action.startswith("Action: "):
            return None

        print(f"{GREEN}Action starts w/ Action: {RESET}")

        try:

            tool_call = action.replace("Action: ", "").strip()
            print(f"{GREEN}Tool call: {tool_call}{RESET}")
            tool_name, args_str = tool_call.split("(", 1)
            print(f"{GREEN}Tool name: {tool_name}{RESET}")
            tool_name = tool_name.strip()
            print(f"{GREEN}Tool name: {tool_name}{RESET}")
            # Parse arguments fron the function call (string)
            # (arg1, arg2, ...) -> ["arg1", "arg2", ...]
            args = {}
            if args_str.strip() != ")":
                args_str = args_str[:-1]
                print(f"{GREEN}Args str: {args_str}{RESET}")
                args_list = args_str.split(",")
                print(f"{GREEN}Args list: {args_list}{RESET}")
                args = {}
                for i, arg in enumerate(args_list):
                    arg_name, arg_type = self.tools[tool_name].arguments[i]
                    print(f"{GREEN}Arg name: {arg_name}{RESET}")
                    print(f"{GREEN}Arg type: {arg_type}{RESET}")
                    # Use a dictionary to map types to casting functions
                    cast_functions = {
                        'int': int,
                        'float': float,
                        'bool': lambda x: x.strip().lower() in ['true', '1', 'yes'],
                        'str': str
                    }
                    # Cast the argument using the appropriate function
                    args[arg_name] = cast_functions.get(arg_type, str)(arg.strip())

                print(f"{GREEN}Args: {args}{RESET}")

            print(f"{GREEN}Tool name: {tool_name}{RESET}")
            print(f"{GREEN}Tool args: {args}{RESET}")

            if tool_name in self.tools:
                result = self.tools[tool_name](**args)
                return f"The tool '{tool_name}' returned: {result}. Use it to proceed."
            else:
                return f"Observation: ERROR - Unknown tool '{tool_name}'"
        except Exception as e:
            print_color(RED, f"Failed to execute tool: {e}")
            return f"Observation: ERROR - Failed to execute tool: {e}"

    def ask(self, prompt: str) -> str:
        """
        Ask the agent a question.
        args:
            - prompt (str): User input.
        returns:
            - str: Agent response.
        """

        print()
        for message in self.history:
            print_color(CYAN, message["content"])
        print()

        self.history.append({"role": "user", "content": prompt})

        messages = [
            {"role": "system", "content": self._system_message()}
        ] + self.history

        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True
        )

        response = ""
        print(CYAN, end="", flush=True)
        for chunk in stream:
            content = chunk.get("message", {}).get("content", "")
            print(content, end="", flush=True)
            response += content
        print(RESET)

        response.replace("Action :", "Action:")
        if "Action:" in response:

            print_color(GREEN, "The agent is attempting to use a tool")

            # Extract the function call from the response
            action = "Action: " + response.split("Action:", 1)[1]
            action = action.split(")", 1)[0] + ")"

            if not action:
                self.history.append({"role": "assistant", "content": response})
                return self.ask(prompt)  # Re-ask with updated context

            observation = self._call_tool(action)
            self.history.append({"role": "assistant", "content": observation})
            return self.ask(prompt)  # Re-ask with updated context

        self.history.append({"role": "assistant", "content": response})

        # Maintain memory limit
        if len(self.history) > self.memory_limit * 2:
            self.history = self.history[-self.memory_limit * 2:]

        return response

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
