SEARCH_BUS_DOCSTRING =  """
    This is the ONLY tool allowed for bus-related queries.

    Purpose:
    - Fetch real bus availability between two cities.

    Parameters:
    - from_city (str): Source city name
    - to_city (str): Destination city name
    - date (str | None):
        • Format: YYYY-MM-DD (ISO 8601), e.g., 2026-01-24
        • If provided → returns buses for that specific date only
        • If None → returns all buses on the route (no date filtering)

    Behavior:
    - With date  → POST /user/search   { from, to, traveldate }
    - Without date → POST /ai/getbus   { from, to }

    STRICT RULES:
    - Always use this tool for bus queries.
    - Do not manually answer.
    - Do not use any other tools.
    """