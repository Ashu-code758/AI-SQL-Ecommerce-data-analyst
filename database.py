import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


FORBIDDEN_KEYWORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "replace",
    "grant",
    "revoke"
]


def run_sql(query):

    query = query.strip()

    if not query:
        return "ERROR: Empty SQL query."

    query_lower = query.lower()

    # Only SELECT queries are allowed
    if not query_lower.startswith("select"):
        return "ERROR: Only SELECT queries are allowed."

    # Block dangerous SQL operations
    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in query_lower:
            return (
                f"ERROR: {keyword.upper()} "
                "operation is not allowed."
            )

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD"),
            database="ecommerce_analysis"
        )

        cursor = connection.cursor()

        cursor.execute(query)

        result = cursor.fetchall()

        return result

    except mysql.connector.Error as e:

        return f"SQL ERROR: {e}"

    finally:

        if "cursor" in locals():
            cursor.close()

        if "connection" in locals() and connection.is_connected():
            connection.close()