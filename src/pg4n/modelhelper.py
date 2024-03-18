import json
import requests

class ModelHelper:
    """
    This class is responsible for sending messages to lambda functions and 
    for handling the answer.
    """
    def __init__(self, lambda_url):
        self.lambda_url = lambda_url

    def send_request(self, query, error, schema):
        """
        Sends a message to lambda function that handles the request and returns models response.
        """
        body = {
            "query": query,
            "error": error,
            "schema": schema
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.lambda_url, headers=headers, data=json.dumps(body))
        return json.loads(response.text)["model_response"]
    