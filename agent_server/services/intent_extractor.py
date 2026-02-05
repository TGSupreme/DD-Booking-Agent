import json
from services.llm import get_llm
from tools.stops import get_all_stops
import re
from agent.prompts.prompts import INTENT_PROMPT
def clean_json(text: str) -> str:
    # remove ```json ... ```
    text = re.sub(r"```json|```", "", text)
    return text.strip()

stops = get_all_stops()

# SYSTEM_PROMPT = f"""
# You are a strict JSON API for a bus search backend.

# Output must be ONLY valid JSON.
# No markdown.
# No explanations.
# No extra text.
# No comments.

# Your job:
# 1. Detect intent.
# 2. Extract source stop, destination stop, and travel date.
# 3. Normalize all extracted values so they are backend-safe.

# INTENTS:
# - search_bus
# - invalid_stop


# STOP RULES:
# 1. Stops MUST be selected ONLY from the VALID_STOPS list.
# 2. NEVER output any stop name not EXACTLY equal to one of the list values.
# 3. Matching must be case-insensitive.
# 4. Always autocorrect typos, spelling mistakes, or phonetic errors.
# 5. Choose the closest valid stop even if the spelling is imperfect.
# 6. Only return invalid_stop if NO reasonable match exists.

# Examples:
# - surat → Surat
# - suraat → Surat
# - ahmdabad → Ahmedabad
# - barodoli → Bardoli


# DATE RULES (VERY IMPORTANT):
# 1. Always interpret the user's date even if messy or misspelled.
# 2. Fix common typos automatically (fab→feb, janury→january, tmrw→tomorrow, etc).
# 3. Understand natural language dates:
#    today, tomorrow, next monday, day after tomorrow, etc.
# 4. Convert ALL dates to STRICT ISO format: YYYY-MM-DD.
# 5. NEVER return raw text like "tomorrow" or "6th feb".
# 6. If year is missing, assume the current year.
# 7. Do not fail because of small date spelling errors.


# VALID_STOPS (whitelist):
# {json.dumps(stops)}


# Output schema (MUST match exactly):
# {{
#   "intent": "search_bus | invalid_stop",
#   "parameters": {{
#       "from": string,
#       "to": string,
#       "traveldate": "YYYY-MM-DD"
#   }}
# }}


# Examples:

# User: Durat to Ahmedabad tomorrow
# Output:
# {{"intent":"search_bus","parameters":{{"from":"Surat","to":"Ahmedabad","traveldate":"2026-02-05"}}}}

# User: find bus surat to ahmedabad 6th fab
# Output:
# {{"intent":"search_bus","parameters":{{"from":"Surat","to":"Ahmedabad","traveldate":"2026-02-06"}}}}

# User: MoonCity to Ahmedabad
# Output:
# {{"intent":"invalid_stop","parameters":{{}}}}
# """


llm = get_llm()


def extract_intent(message: str) -> dict:
    

    prompt = INTENT_PROMPT.format_messages(
        stops=json.dumps(stops),
        message=message
    )
    # print("FInal query to llm : ", prompt)
    print("Calling INTENT EXTRSCTOR LLM......")
    response = llm.invoke(prompt)
    content = response.content

    print("RAW RESPONSE(CONTENT)(INtent Extractor):", content)

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
