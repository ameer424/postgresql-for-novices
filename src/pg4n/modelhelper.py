import json
import requests

class ModelHelper:
    """
    This class is responsible for sending messages to lambda functions and 
    for handling the answer.
    """
    def __init__(self, lambda_url, apikey):
        self.lambda_url = lambda_url + "readFromModel"
        self.apikey = apikey

    def send_request(self, query, error, schema):
        """
        Sends a message to lambda function that handles the request and returns models response.
        """
        body = {
            "query": query,
            "error": error,
            "schema": schema
        }
        
        headers = {'Content-Type': 'application/json',
                   'x-api-key': self.apikey}
               
        response = requests.post(self.lambda_url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            return (True,json.loads(response.text)["model_response"])        
        return (False,response.json()) 
    