sql_tool = {

    "type": "function",

    "function": {

        "name": "run_sql",

        "description":
            "Execute a read-only MYSQL SELECT query "
            "on the ecommerce_analysis database "
            "and return the result",

        "parameters": {

            "type": "object",

            "properties": {

                "query": {

                    "type": "string",

                    "description":
                        "A valid MYSQL SELECT query."
                }
            },

            "required": ["query"]
        }
    }
}


calculator_tool = {

    "type": "function",

    "function": {

        "name": "calculate",

        "description":
            "Perform a mathematical calculation.",

        "parameters": {

            "type": "object",

            "properties": {

                "expression": {

                    "type": "string",

                    "description":
                        "Mathematical expression to calculate."
                }
            },

            "required": ["expression"]
        }
    }
}


profit_margin_tool = {

    "type": "function",

    "function": {

        "name": "calculate_profit_margin",

        "description":
            "Calculate profit margin using profit and sales.",

        "parameters": {

            "type": "object",

            "properties": {

                "profit": {
                    "type": "number"
                },

                "sales": {
                    "type": "number"
                }
            },

            "required": [
                "profit",
                "sales"
            ]
        }
    }
}


TOOLS = [
    sql_tool,
    calculator_tool,
    profit_margin_tool
]