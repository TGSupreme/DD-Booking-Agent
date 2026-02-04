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

Convert the bus search result JSON into a friendly, natural message.

Guidelines:
- Start with a short conversational sentence
- Mention number of buses found
- Keep tone simple and concise
- Avoid long descriptions

For each bus, you MUST use EXACTLY this Markdown format:

### Bus <number>: <operator> (<bus_number>)
- Departure: <departure_time>
- Arrival: <arrival_time>
- Price: ₹<price>
- Total seats: <total_seats>
- Available seats: <available_seats>
- Amenities: <comma separated list>

After listing all buses, add a short summary (max 2 sentences) comparing:
- cheapest bus
- earliest or fastest option

Rules:
- Do not add extra sentences inside bus blocks
- Keep response compact
- Do NOT output JSON
- Do NOT explain anything
"""

def format_bus_list(data: dict) -> str:
    prompt = [
        ("system", BUS_FORMAT_PROMPT),
        ("user", json.dumps(data, indent=2))
    ]

    print("Calling Formatter LLM......")
    response = llm.invoke(prompt)
    content = response.content
    

    if isinstance(response.content, str):
        return content.strip()

    if isinstance(response.content, list):
        for item in content:
            if item.get("type") == "text":
                return item["text"].strip()

    return "Sorry, I couldn't format the bus results."
