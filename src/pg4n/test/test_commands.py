"""
Test commands in commands.py
"""
from ..commands import main
import random
import unittest
from unittest.mock import patch
import re

def test_create_key():
    random_number = random.randint(1, 10000)
    with patch('builtins.input', side_effect=["address https://rb7711t55l.execute-api.us-east-1.amazonaws.com/", 
                                              "apikey example_master_key_123", 
                                              "create", f"id_{random_number}", "integration_test", "", 
                                              "get", f"id_{random_number}", "", 
                                              "delete", f"id_{random_number}", "", 
                                              "get", f"id_{random_number}", "", 
                                              "setapi off", 
                                              "setapi on", 
                                              "exit"]):
        with patch("builtins.print") as print_calls:
            main()
            output = ""
            regex_pattern_create_and_get_response = "ID: .*, Name: .*, Key: .*, Tokens: .*"

            for call in print_calls.call_args_list:
                output += str(call[0])
            assert ( re.search(regex_pattern_create_and_get_response, output) )
            assert ( "API state set to: OFF" in output )
            assert ( "API state set to: ON" in output )
            assert ( "was not found in database" in output )