from orchestrator import run_agent


# Test queries

test_queries = [
    # Query 1: Should trigger → list_available_apis only
    "What APIs are available on the portal?",

    # Query 2: Should trigger → list_available_apis → get_swagger_for_api
    "What can I do with the Shipping API?",

    # Query 3: Should trigger → get_endpoint_details (or chain from list first)
    "How do I create a shipment using the Shipping API v2?",
]


if __name__ == "__main__":
    for i, query in enumerate(test_queries, 1):
        print("\n" + "=" * 60)
        print(f"TEST {i}: {query}")
        print("=" * 60)

        answer = run_agent(query)

        print("\n" + "-" * 60)
        print(f"FINAL ANSWER:\n{answer}")
        print("-" * 60)