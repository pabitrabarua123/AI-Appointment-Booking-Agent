import json

from openai import OpenAI
from dotenv import load_dotenv

from tools import (
    get_available_slots,
    get_therapist_details
)


# --------------------------------
# Load environment variables
# --------------------------------

load_dotenv()

client = OpenAI()


# --------------------------------
# Tool definitions
# --------------------------------

tools = [
    {
        "type": "function",
        "name": "get_available_slots",
        "description": "Get available therapy appointment slots for a specific date.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The appointment date in YYYY-MM-DD format."
                }
            },
            "required": ["date"]
        }
    },
    {
        "type": "function",
        "name": "get_therapist_details",
        "description": "Get the details of a therapist, including education and area of expertise.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the therapist."
                }
            },
            "required": ["name"]
        }
    }
]


# --------------------------------
# Map tool names to Python functions
# --------------------------------

available_functions = {
    "get_available_slots": get_available_slots,
    "get_therapist_details": get_therapist_details,
}


# --------------------------------
# AI Agent
# --------------------------------


def run_agent(user_message, history=None):
    if history is None:
        history = []

    # Build the full conversation for the AI.
    conversation = [
        {
            "role": item["role"],
            "content": item["content"]
        }
        for item in history
        if item["role"] in ("user", "assistant")
    ]

    # Add the latest user message.
    conversation.append({
        "role": "user",
        "content": user_message
    })

    # Send the entire conversation to OpenAI.
    response = client.responses.create(
        model="gpt-6-luna",
        input=conversation,
        tools=tools
    )

    tool_outputs = []

    for item in response.output:
        if item.type == "function_call":
            print("Tool:", item.name)
            print("Arguments:", item.arguments)

            arguments = json.loads(item.arguments)

            function = available_functions[item.name]
            result = function(**arguments)

            print("Result:", result)

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": str(result)
            })

    # If the AI called a tool, send the result back to OpenAI.
    if tool_outputs:
        final_response = client.responses.create(
            model="gpt-6-luna",
            previous_response_id=response.id,
            input=tool_outputs
        )

        return final_response.output_text

    # If no tool was called, return the AI's response directly.
    return response.output_text
