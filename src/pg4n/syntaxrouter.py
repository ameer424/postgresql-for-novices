from typing import Any, Optional, Type

import psycopg
from sqlglot import exp

from .config_values import ConfigValues

from .get_postre_schema import Postgres_schema

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
        schema_address = "host=" + self.pg_host + " port=" + self.pg_port + " dbname="+ self.pg_name  + " user=" + self.pg_user + " password=" +self.pg_pass

        #print("schema_address:" + schema_address)
        #postgres_schema = Postgres_schema.get_postgres_schema("host=127.0.0.1 port=5432 dbname=template1 user=root password=test ")
        postgres_schema = Postgres_schema.get_postgres_schema("host=/var/run/postgresql port=5432 dbname=template1 user=root password=test ")
        #print("Schema: " + "".join(str(line) for line in postgres_schema))
        tunnistus = "Ahaa, uusi syntax virhe löydetty."
        täydennys = "\n tähän tulee LLM generoimat tilpehöörit"
        #print(sql_query + " " + sql_error)       
        return ""