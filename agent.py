import json

from config import client, MODEL
from schema import DATABASE_SCHEMA
from tools import TOOLS
from database import run_sql
from calculations import calculate, calculate_profit_margin


SYSTEM_PROMPT = f"""
You are an AI Data Analyst Agent.

You answer business questions using the ecommerce database.

DATABASE SCHEMA:
{DATABASE_SCHEMA}

RULES:

1. Use run_sql whenever database information is required.
2. Prefer SQL for aggregations, filtering, grouping, ranking,
   percentages, comparisons, trends, and business metrics.
3. Use calculate only when SQL is not suitable.
4. Use calculate_profit_margin when appropriate.
5. Use previous conversation context when the user refers to
   previous results using words such as:
   "it", "its", "that", "this", "they", "them",
   "same country", "same product", etc.
6. Never invent database information.
7. Use only columns available in the database schema.
8. Only read data. Never modify the database.
9. Keep answers clear and business-friendly.
10. If required information is unavailable, say so instead of guessing.
11. Only state business observations directly supported by the query result.
12. Do not invent trends, causes, or insights that are not supported by data.
"""


def run_agent(messages, return_trace=False):

    # Store tool information for Streamlit
    trace = {
        "sql_queries": [],
        "database_results": [],
        "tools_used": []
    }

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0.2
        )

        message = response.choices[0].message

        # Convert SDK message to normal dictionary
        message_dict = message.model_dump(exclude_none=True)

        messages.append(message_dict)

        # ---------------------------------
        # Final AI Answer
        # ---------------------------------

        if not message.tool_calls:

            answer = message.content

            if return_trace:

                return {
                    "answer": answer,
                    "trace": trace
                }

            return answer

        # ---------------------------------
        # Tool Calls
        # ---------------------------------

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            # ---------------------------------
            # SQL Tool
            # ---------------------------------

            if tool_name == "run_sql":

                query = arguments["query"]

                trace["tools_used"].append("SQL")

                trace["sql_queries"].append(query)

                print("\nTool: run_sql")
                print("\nGenerated SQL:")
                print(query)

                result = run_sql(query)

                trace["database_results"].append(result)

                print("\nDatabase Result:")
                print(result)

            # ---------------------------------
            # Calculator Tool
            # ---------------------------------

            elif tool_name == "calculate":

                expression = arguments["expression"]

                trace["tools_used"].append("Calculator")

                print("\nTool: calculate")
                print("\nExpression:")
                print(expression)

                result = calculate(expression)

                print("\nCalculation Result:")
                print(result)

            # ---------------------------------
            # Profit Margin Tool
            # ---------------------------------

            elif tool_name == "calculate_profit_margin":

                profit = arguments["profit"]
                sales = arguments["sales"]

                trace["tools_used"].append(
                    "Profit Margin Calculator"
                )

                print("\nTool: calculate_profit_margin")

                result = calculate_profit_margin(
                    profit,
                    sales
                )

                print("\nProfit Margin:")
                print(result)

            else:

                result = "Unknown tool."

            # ---------------------------------
            # Send Tool Result Back to AI
            # ---------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )