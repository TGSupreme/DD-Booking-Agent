# def format_bus_list(data: dict) -> str:
#     if not data.get("success"):
#         print(data)
#         return "Something went wrong while fetching buses."

#     buses = data.get("buses", [])

#     if not buses:
#         return "No buses found for this route and date."

#     lines = ["🚌 Available buses:\n"]

#     for i, b in enumerate(buses, 1):
#         line = (
#             f"{i}. {b['busname']} | ₹{b['price']} | "
#             f"{b['availableseat']} seats | "
#             f"{b['fromtime']} → {b['totime']}"
#         )
#         lines.append(line)

#     return "\n".join(lines)

from services.llm import get_llm
import json

llm = get_llm()

BUS_FORMAT_PROMPT = """
You are a helpful travel assistant.

Convert the given bus search result JSON into a friendly conversational message.

Rules:
- Speak naturally like a human assistant
- Summarize nicely
- Mention number of buses found
- Highlight price, time, and seats
- If no buses, politely inform user
- DO NOT output JSON
- DO NOT explain anything
"""

def format_bus_list(data: dict) -> str:
    prompt = [
        ("system", BUS_FORMAT_PROMPT),
        ("user", json.dumps(data, indent=2))
    ]

    response = llm.invoke(prompt)

    if isinstance(response.content, str):
        return response.content.strip()

    if isinstance(response.content, list):
        for item in response.content:
            if item.get("type") == "text":
                return item["text"].strip()

    return "Sorry, I couldn't format the bus results."
