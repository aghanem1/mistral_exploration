import json
from config import client, MODEL, TEMPERATURE, TOP_P, MAX_ITERATIONS
from tools import names_to_functions
from tool_definitions import tools


# System prompt

SYSTEM_PROMPT = """You are an API Portal assistant for CMA CGM.
Your job is to help users discover APIs, understand endpoints, and build request examples.

You have 3 tools available:

1. list_available_apis — Use this FIRST when the user asks what APIs exist,
   or when you need to find the correct API name before doing anything else.

2. get_swagger_for_api — Use this to retrieve the full specification of a specific API.
   You need the exact api_name. If you don't have it, call list_available_apis first.

3. get_endpoint_details — Use this to get details about a specific endpoint:
   HTTP method, parameters, request body schema.
   You need both api_name and endpoint_path.

Rules:
- NEVER make up API details. Always use the tools to get real data.
- If the user asks a vague question like "how do I ship something?",
  start by listing APIs, then find the right one, then get the endpoint details.
- When you have enough information, give the user a clear, helpful answer.
- If a tool returns an error, tell the user what went wrong and suggest next steps.
"""


def run_agent(user_message: str) -> str:
    """
    Main entry point. The backend calls this with the user's message.
    Returns the final answer as a string.

    The loop follows Mistral's function calling flow:
      system + user → model → [tool_call → tool_result → model] → final answer
    """

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i + 1} ---")

        response = client.chat.complete(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",  
            parallel_tool_calls=False,
            temperature=TEMPERATURE,
            top_p=TOP_P,
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:

            messages.append(assistant_message)

            for tool_call in assistant_message.tool_calls:

                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"  Tool called: {function_name}")
                print(f"  Arguments:   {function_args}")

                if function_name in names_to_functions:
                    result = names_to_functions[function_name](function_args)
                else:
                    result = json.dumps({"error": f"Unknown tool: {function_name}"})

                print(f"  Result:      {result[:150]}...")

                messages.append({
                    "role": "tool",
                    "name": function_name,
                    "content": result,
                    "tool_call_id": tool_call.id,
                })


        else:
            final_answer = assistant_message.content
            print(f"\n  Final answer: {final_answer[:200]}...")
            return final_answer

    return "I wasn't able to complete your request. Please try rephrasing your question."