from typing import Any, Optional, Type

import psycopg
from sqlglot import exp

from .config_values import ConfigValues

from .get_postre_schema import Postgre_schema
from .modelhelper import ModelHelper

class SyntaxRouter:
    def __init__(
        self,
        pg_host: str,
        pg_port: str,
        pg_user: str,
        pg_pass: str,
        pg_name: str,
        config_values: Optional[ConfigValues],
    ):
        """Initialize Postgres connection with given paramaters."""
        self.pg_host: str = pg_host
        self.pg_port: str = pg_port
        self.pg_user: str = pg_user
        self.pg_pass: str = pg_pass
        self.pg_name: str = pg_name
        self.config_values: Optional[ConfigValues] = config_values
    
    
    def run_analysis(self, sql_error: str,sql_query: str) -> str:
        """
        Function that calls ModelHelper class with all the attributes it needs
        Returns LLM answer to pg4n
        """
        if self.config_values is not None:  
            if self.config_values.get("LambdaAddress") is not None and self.config_values.get("APIKey") is not None:
                schema_address = "host=" + self.pg_host + " port=" + self.pg_port + " dbname="+ self.pg_name  + " user=" + self.pg_user
                postgre_schema = Postgre_schema.get_postgre_schema(schema_address)
                schema = "".join(str(line) for line in postgre_schema)
                model_helper = ModelHelper(self.config_values.get("LambdaAddress"),self.config_values.get("APIKey"))
                llm_answer = model_helper.send_request(sql_query, sql_error, schema)
                if llm_answer[0] == True:
                    return llm_answer[1]
                return "Error: " + llm_answer[1]      
        return "Syntax Router Error: Missing Address, Apikey or both!!"