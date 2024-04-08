import psycopg
from psycopg import OperationalError

class Postgre_schema:
    """
    Class for getting postressql table schemas to help LLM give better answers.
    """
    def get_postgre_schema(connection_data):
        """
        Gets full schema at postresql
        """
        try:
            # Establish a connection to the PostgreSQL database
            conn = psycopg.connect(
                connection_data
            )

            # Fetch the schema for tables
            cursor = conn.execute("""
                SELECT table_schema, table_name, column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema NOT IN ('pg_catalog', 'information_schema');
            """)

            schema = cursor.fetchall()  # Fetch all rows

            # Close the cursor and connection
            cursor.close()
            conn.close()

            return schema

        except OperationalError as e:
            print(f"Error connecting to PostgreSQL: {e}")
