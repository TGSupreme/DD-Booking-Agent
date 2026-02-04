from tools.search_bus import search_bus
from tools.stops import get_all_stops
from services.llm import get_llm
import json
from datetime import date
from services.llm import get_llm
from agent.formatter import format_bus_list


def handle_search_bus(message):
    intent = extract_params(message)
    payload = intent['parameters']
    if (intent["intent"] == "invalid_stop"):
        invalid_stop = (intent["parameters"])['invalid_stop']
        return f"{invalid_stop} is not a valid station"
    
    else:
        print(payload)
        apiResponse =  search_bus(payload)
        print(apiResponse)
        return format_bus_list(apiResponse)


def extract_params(message):
    stops = get_all_stops()
    TODAY = date.today().isoformat()
    llm = get_llm()
    
    SYSTEM_PROMPT = f"""
You are a strict JSON API for a bus search backend.

Output must be ONLY valid JSON.
No markdown.
No explanations.
No extra text.
No comments.

TODAY IS: {TODAY}

Your job:
1. Detect intent.
2. Extract source stop, destination stop, and travel date.
3. Normalize all extracted values so they are backend-safe.

INTENTS:
- search_bus
- invalid_stop

INTENT RULES:
- Use "search_bus" ONLY if from, to, and traveldate are ALL confidently extracted.
- If either from or to cannot be matched → intent = invalid_stop.
- If date is missing or cannot be resolved → intent = invalid_stop.

STOP RULES:
1. Stops MUST be selected ONLY from the VALID_STOPS list.
2. NEVER output any stop name not EXACTLY equal to one of the list values.
3. Matching must be case-insensitive.
4. Always autocorrect typos, spelling mistakes, or phonetic errors.
5. Choose the closest valid stop even if the spelling is imperfect.
6. Only return invalid_stop if NO reasonable match exists.
7. If a stop cannot be reasonably matched, capture the ORIGINAL user-provided stop text as invalid.
8. Do NOT guess or autocorrect stop names in invalid_stop cases.

DATE RULES (VERY IMPORTANT):
1. Always interpret the user's date even if messy or misspelled.
2. Fix common typos automatically (fab→feb, janury→january, tmrw→tomorrow, etc).
3. Understand natural language dates:
   today, tomorrow, next monday, day after tomorrow, etc.
4. Convert ALL dates to STRICT ISO format: YYYY-MM-DD.
5. NEVER return raw text like "tomorrow" or "6th feb".
6. If year is missing, assume the current year.
7. Resolve relative dates using TODAY.
8. Do not fail because of small date spelling errors.

VALID_STOPS (whitelist):
{json.dumps(stops)}

OUTPUT SCHEMA (MUST match exactly):
    {{
  "intent": "search_bus | invalid_stop",
  "parameters": {{
    "from": string,
    "to": string,
    "traveldate": "YYYY-MM-DD",
    "invalid_stop": string,
    "invalid_stops": array
  }}
}}

SCHEMA RULES:
- For intent = search_bus:
  - parameters MUST contain only: from, to, traveldate
  - parameters MUST NOT contain invalid_stop or invalid_stops

- For intent = invalid_stop:
  - parameters MUST NOT contain from, to, or traveldate
  - If exactly one stop is invalid → use "invalid_stop" (string)
  - If more than one stop is invalid → use "invalid_stops" (array of strings)
  - The value(s) MUST be the original user-provided stop name(s)

EXAMPLES:

User: Durat to Ahmedabad tomorrow
Output:
{{"intent":"search_bus","parameters":{{"from":"Surat","to":"Ahmedabad","traveldate":"2026-02-05"}}}}

User: MoonCity to Ahmedabad
Output:
{{"intent":"invalid_stop","parameters":{{"invalid_stop":"MoonCity"}}}}

User: MoonCity to Ahmdd
Output:
{{"intent":"invalid_stop","parameters":{{"invalid_stops":["MoonCity","Ahmdd"]}}}}
"""

    prompt = [
        ("system", SYSTEM_PROMPT),
        ("user", message)
    ]

    response = llm.invoke(prompt)
    

    try:
        intent = json.loads(response.content.strip())
        return intent

    except json.JSONDecodeError:
        raise ValueError(f"LLM returned invalid JSON: {response.content}")
    
