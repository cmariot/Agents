from tools.Tool import tool


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@tool
def introduce_myself() -> str:
    """Introduce myself."""
    return "Hello, I am a chatbot. I can perform some basic operations."
