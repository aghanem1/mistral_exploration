tools = [
    # Tool 1: List available APIs
    {
        "type": "function",
        "function": {
            "name": "list_available_apis",
            "description": (
                "Returns a list of all API products available on the portal. "
                "Each entry includes the product name, API name, and a short description. "
                "Use this tool when the user asks what APIs exist, wants an overview, "
                "or when you need to find the correct API name before using other tools."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    # Tool 2: Get swagger for a specific API
    {
        "type": "function",
        "function": {
            "name": "get_swagger_for_api",
            "description": (
                "Retrieves the full OpenAPI/Swagger specification for a given API product. "
                "Returns all available endpoints, methods, and schemas. "
                "Use this when the user asks about a specific API's capabilities, "
                "or when you need to discover what endpoints are available before "
                "drilling into a specific one. "
                "You must provide the api_name — if you don't know it, "
                "call list_available_apis first."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "api_name": {
                        "type": "string",
                        "description": "The name of the API product (e.g. 'Shipping API v2').",
                    },
                },
                "required": ["api_name"],
            },
        },
    },

    # Tool 3: Get endpoint details
    {
        "type": "function",
        "function": {
            "name": "get_endpoint_details",
            "description": (
                "Given an API name and an endpoint path, returns detailed information: "
                "HTTP method, summary, description, required and optional parameters, "
                "and the request body schema if applicable. "
                "Use this when the user asks how to call a specific endpoint, "
                "wants to know what parameters are needed, "
                "or asks you to build a request example. "
                "You must provide api_name. The endpoint_path can be partial "
                "(e.g. '/shipments' will match '/v2/shipments')."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "api_name": {
                        "type": "string",
                        "description": "The name of the API product (e.g. 'Shipping API v2').",
                    },
                    "endpoint_path": {
                        "type": "string",
                        "description": "The endpoint path to look up (e.g. '/v2/shipments'). Can be partial.",
                    },
                },
                "required": ["api_name", "endpoint_path"],
            },
        },
    },
]