import json


# Dummy data (replace with real API calls later)

API_CATALOG = [
    {
        "product": "Shipping",
        "api_name": "Shipping API v2",
        "description": "Track shipments, get rates, and book containers.",
    },
    {
        "product": "Billing",
        "api_name": "Billing API v1",
        "description": "Retrieve invoices, payment status, and account balances.",
    },
    {
        "product": "Booking",
        "api_name": "Booking API v3",
        "description": "Create, update, and cancel container bookings.",
    },
]

# Mini swagger specs keyed by API name
SWAGGER_DB = {
    "shipping api v2": {
        "openapi": "3.0.0",
        "info": {"title": "Shipping API", "version": "2.0.0"},
        "paths": {
            "/v2/shipments": {
                "get": {
                    "summary": "List all shipments",
                    "description": "Returns a paginated list of shipments for the authenticated user.",
                    "parameters": [
                        {"name": "status", "in": "query", "required": False, "type": "string", "description": "Filter by status: active, completed, cancelled."},
                        {"name": "page", "in": "query", "required": False, "type": "integer", "description": "Page number for pagination."},
                    ],
                },
                "post": {
                    "summary": "Create a shipment",
                    "description": "Creates a new shipment booking.",
                    "parameters": [],
                    "request_body": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["origin", "destination", "container_type"],
                                    "properties": {
                                        "origin": {"type": "string", "description": "Origin port code (e.g. FRMRS)."},
                                        "destination": {"type": "string", "description": "Destination port code (e.g. CNSHA)."},
                                        "container_type": {"type": "string", "description": "Container type: 20GP, 40GP, 40HC."},
                                        "reference_number": {"type": "string", "description": "Optional customer reference."},
                                    },
                                }
                            }
                        },
                    },
                },
            },
            "/v2/shipments/{shipment_id}": {
                "get": {
                    "summary": "Get shipment details",
                    "description": "Returns full details for a single shipment by ID.",
                    "parameters": [
                        {"name": "shipment_id", "in": "path", "required": True, "type": "string", "description": "The unique shipment identifier."},
                    ],
                },
            },
        },
    },
    "billing api v1": {
        "openapi": "3.0.0",
        "info": {"title": "Billing API", "version": "1.0.0"},
        "paths": {
            "/v1/invoices": {
                "get": {
                    "summary": "List invoices",
                    "description": "Returns all invoices for the authenticated account.",
                    "parameters": [
                        {"name": "from_date", "in": "query", "required": False, "type": "string", "description": "Start date filter (YYYY-MM-DD)."},
                        {"name": "to_date", "in": "query", "required": False, "type": "string", "description": "End date filter (YYYY-MM-DD)."},
                    ],
                },
            },
        },
    },
    "booking api v3": {
        "openapi": "3.0.0",
        "info": {"title": "Booking API", "version": "3.0.0"},
        "paths": {
            "/v3/bookings": {
                "post": {
                    "summary": "Create a booking",
                    "description": "Creates a new container booking request.",
                    "parameters": [],
                    "request_body": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["origin", "destination", "commodity", "container_type"],
                                    "properties": {
                                        "origin": {"type": "string", "description": "Origin port code."},
                                        "destination": {"type": "string", "description": "Destination port code."},
                                        "commodity": {"type": "string", "description": "Type of goods being shipped."},
                                        "container_type": {"type": "string", "description": "Container size: 20GP, 40GP, 40HC."},
                                    },
                                }
                            }
                        },
                    },
                },
            },
        },
    },
}


# Tool 1: List available APIs

def list_available_apis() -> str:
    return json.dumps({"apis": API_CATALOG})


# Tool 2: Get swagger for a specific API

def get_swagger_for_api(api_name: str) -> str:
    key = api_name.strip().lower()

    swagger = SWAGGER_DB.get(key)

    if not swagger:
        for db_key, db_val in SWAGGER_DB.items():
            if key in db_key or db_key in key:
                swagger = db_val
                break

    if swagger:
        return json.dumps(swagger)

    return json.dumps({"error": f"No swagger found for '{api_name}'. Use list_available_apis to see valid names."})


# Tool 3: Get endpoint details from swagger

def get_endpoint_details(api_name: str, endpoint_path: str) -> str:

    swagger_raw = get_swagger_for_api(api_name)
    swagger = json.loads(swagger_raw)

    if "error" in swagger:
        return json.dumps(swagger)

    paths = swagger.get("paths", {})

    path_data = paths.get(endpoint_path)

    if not path_data:
        clean = endpoint_path.strip().lower()
        for p_key, p_val in paths.items():
            if clean in p_key.lower() or p_key.lower() in clean:
                path_data = p_val
                endpoint_path = p_key
                break

    if not path_data:
        available = list(paths.keys())
        return json.dumps({
            "error": f"Endpoint '{endpoint_path}' not found.",
            "available_endpoints": available,
        })

    result = []
    for method, details in path_data.items():
        entry = {
            "endpoint": endpoint_path,
            "method": method.upper(),
            "summary": details.get("summary", ""),
            "description": details.get("description", ""),
            "parameters": details.get("parameters", []),
        }
        if "request_body" in details:
            entry["request_body"] = details["request_body"]

        result.append(entry)

    return json.dumps({"endpoints": result})


# Function registry (used by the orchestrator)

names_to_functions = {
    "list_available_apis": lambda args: list_available_apis(),
    "get_swagger_for_api": lambda args: get_swagger_for_api(**args),
    "get_endpoint_details": lambda args: get_endpoint_details(**args),
}