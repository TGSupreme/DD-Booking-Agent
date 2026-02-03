import json
from services.llm import get_llm
from tools.stops import get_all_stops
import re

def clean_json(text: str) -> str:
    # remove ```json ... ```
    text = re.sub(r"```json|```", "", text)
    return text.strip()

stops = get_all_stops()
SYSTEM_PROMPT = f"""
You are a strict JSON API.

Output must be ONLY valid JSON.
No markdown. No explanations. No extra text.

Your job:
1. Detect intent.
2. Extract stops and date.
3. Stops MUST be selected ONLY from the VALID_STOPS list.
4. If user input contains typos, choose the closest matching stop from the list.
5. NEVER output a stop name that is not EXACTLY one of the list values.
6. If no match exists, return:
{{"intent":"invalid_stop","parameters":{{}}}}

VALID_STOPS (whitelist):
{json.dumps(stops)}

Output schema:
{{
  "intent": "search_bus | invalid_stop",
  "parameters": {{
      "from": string,
      "to": string,
      "traveldate": string
  }}
}}

Examples:

User: Durat to Ahmedabad tomorrow
Output:
{{"intent":"search_bus","parameters":{{"from":"Surat","to":"Ahmedabad","traveldate":"tomorrow"}}}}

User: MoonCity to Ahmedabad
Output:
{{"intent":"invalid_stop","parameters":{{}}}}
"""


llm = get_llm()


def extract_intent(message: str) -> dict:
    
    print(SYSTEM_PROMPT)

    prompt = [
        ("system", SYSTEM_PROMPT),
        ("user", message)
    ]

    response = llm.invoke(prompt)
    content = response.content

    print("RAW RESPONSE:", content)

    try:
        # Case 1: content is already a string
        if isinstance(content, str):
            return json.loads(clean_json(content))

        # Case 2: content is a list of message blocks
        if isinstance(content, list):
            for item in content:
                if item.get("type") == "text":
                    return json.loads(clean_json(item["text"]))

        return {"intent": "unknown", "parameters": {}}

    except Exception as e:
        print("JSON parse error:", e)
        return {"intent": "unknown", "parameters": {}}
