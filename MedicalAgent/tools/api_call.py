# Generate api calls to get the data from the internet
from smolagents import Tool
import requests


class ApiCallTool(Tool):
    """
    A tool for making API calls.
    """

    name = "api_call"
    description = """
    A tool for making API calls.

    This class allows for GET and POST requests to a specified URL
    """

    inputs = {
        "method": {
            "type": "string",
            "description": "The HTTP method to use for the API call.",
        },
        "url": {
            "type": "string",
            "description": "The URL to make the API call to.",
        }
    }

    output_type = "string"

    def forward(self, method: str, url: str):
        try:
            response = requests.request(method, url)
            response.raise_for_status()
            return str(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


if __name__ == "__main__":
    tool = ApiCallTool()
    response = tool.forward("GET", "https://api.example.com/data")
    if response:
        print(response)
