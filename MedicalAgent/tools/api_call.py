# Generate api calls to get the data from the internet
from smolagents.tools import Tool
import requests


class ApiCallTool(Tool):
    """
    A tool for making API calls.

    This class allows for GET and POST requests to a specified URL,
    along with optional parameters for headers,
    query parameters, request body, and other settings.
    """

    name = "api_call"
    description = """
    A tool for making API calls.

    This class allows for GET and POST requests to a specified URL,
    along with optional parameters for headers,
    query parameters, request body, and other settings.
    """
    inputs = {
        "method": {
            "type": "string",
            "description": "HTTP method (GET or POST)"
        },
        "url": {
            "type": "string",
            "description": "The URL to make the request to"
        },
        "headers": {
            "type": "object",
            "description": "Optional headers for the request"
        },
        "params": {
            "type": "object",
            "description": "Optional query parameters for the request"
        },
        "data": {
            "type": "object",
            "description": "Optional data for POST requests"
        },
        "json": {
            "type": "object",
            "description": "Optional JSON data for POST requests"
        }
    }
    output_type = "string"

    def __init__(self, method: str = 'GET', url: str = None, **kwargs):
        self.method = method
        self.url = url

    def api_call(self, method: str = "GET", url: str = "") -> str:
        try:
            response = requests.request(method, url)
            response.raise_for_status()
            return str(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def forward(self, method: str, url: str, **kwargs):
        self.method = method
        self.url = url
        return self.api_call(**kwargs)


# Example usage:
if __name__ == "__main__":
    tool = ApiCallTool()
    # response = tool.forward("GET", "https://api.example.com/data")
    # if response:
        # print(response)  # Changed from response.json() to response to reflect string output
