from typing import Any, Optional, Type

import psycopg
from sqlglot import exp

from .config_values import ConfigValues

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
    
    
    def run_analysis(self, sql_error: str,sql_query: str, sql_schema: str) -> str:
        print("Schema: " + sql_schema)
        tunnistus = "Ahaa, uusi syntax virhe löydetty."
        täydennys = "\n tähän tulee LLM generoimat tilpehöörit"        
        return sql_query + " " + sql_error