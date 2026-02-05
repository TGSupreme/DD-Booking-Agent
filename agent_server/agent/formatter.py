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
from agent.prompts.prompts import SEARCH_BUS_FORMATTER_PROMPT
llm = get_llm()


def format_bus_list(data: dict) -> str:
    prompt = [
        ("system", SEARCH_BUS_FORMATTER_PROMPT),
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
