import json
import requests

class ModelHelper:
    """
    This class is responsible for sending messages to lambda functions and 
    for handling the answer.

    Returns:
            LLM:s message or error message
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

        # Check if http responce 200, 500 or something else (4XX).       
        response = requests.post(self.lambda_url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            return (True,json.loads(response.text)["model_response"])
        elif response.status_code == 500:
            return (False,"Unexpected error in AWS!") 
        else:
            res_json = response.json()                 
            return (False,res_json["message"]) 
    