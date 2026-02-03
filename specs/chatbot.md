# QuickBus AI Chatbot Module (Read-Only Assistant)

## Overview

QuickBus AI Chatbot is a **read-only conversational assistant** for the QuickBus system.

It helps users **retrieve information** using natural language.

The Chatbot can:

- search buses
- check routes
- view timings
- check seat availability
- view ticket status
- answer general queries

It NEVER performs actions like booking or cancelling.

---

# Goal

Enable users to ask questions like:

"Show buses from Surat to Ahmedabad"  
"What time does the 7 AM bus arrive?"  
"Are seats available tomorrow?"  
"Check my ticket status"

The Chatbot should:

1. Understand the question
2. Extract parameters
3. Call backend GET APIs
4. Return formatted answers

---

# Core Principle

LLM → reasoning only  
Chatbot → orchestration only  
Backend → data provider only  

Chatbot behaves like a **smart information retriever**.

It does NOT modify any data.

---

# Final Architecture

```
Streamlit (UI)
      ↓
AI Chatbot Server (Flask + LangChain + Gemini)
      ↓
Backend APIs (GET only)
```

---

# Responsibilities

## 1. Streamlit (Frontend – Permanent UI)

Responsibilities:
- send user messages
- display chatbot replies
- show search results

Rules:
- no business logic
- no DB calls
- no direct API logic

Only handles UI rendering.

---

## 2. AI Chatbot Server (Your Work Area)

Acts as:
Intelligence + routing layer

Responsibilities:
- receive user messages
- call Gemini LLM
- detect user intent
- extract parameters (source, destination, date, etc.)
- choose correct API wrapper
- call backend GET APIs
- format readable responses

Never:
- access database
- modify data
- perform bookings
- cancel tickets
- update records

Chatbot is strictly read-only.

---

## 3. Backend (Black Box)

Acts as:
Data provider

Chatbot only:
- sends GET requests
- receives data

Chatbot MUST NOT depend on backend internals.

Treat backend as:
Input → Output API system only.

---

# Golden Rules (Strict)

1. Chatbot NEVER accesses DB
2. Chatbot NEVER contains business logic
3. Chatbot ONLY calls GET APIs
4. Chatbot NEVER modifies data
5. LLM NEVER executes code
6. LLM ONLY returns reasoning/text
7. All models run via cloud APIs only
8. Backend is the single source of truth

If any rule breaks → architecture is wrong

---

# Tech Stack

## Frontend
- Streamlit

## Chatbot Server
- Python 3.10
- Flask
- LangChain
- langchain-google-genai
- requests / httpx

## LLM Provider
- Google Gemini API (hosted)

---

# LLM Configuration (Official Setup)

We use Gemini through LangChain.

## services/llm.py

```python
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm():

    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3
    )

    return chat_model
```

---

# Calling the LLM

```python
from langchain_core.messages import HumanMessage

response = llm.invoke([
    HumanMessage(content="Show buses from Surat to Ahmedabad")
])

print(response.content)
```

Always pass message objects.  
Do NOT pass plain strings.

---

# Chatbot Workflow

For every message:

Step 1 → Receive user query  
Step 2 → Send to LLM  
Step 3 → Detect intent  
Step 4 → Extract parameters  
Step 5 → Choose GET tool  
Step 6 → Call backend API  
Step 7 → Return formatted answer  

Flow:

```
User
 ↓
LLM reasoning
 ↓
Tool selection (GET only)
 ↓
Backend API call
 ↓
Information response
```

---

# Tools Design (Critical)

Each tool = exactly one backend GET API wrapper.

Tools MUST:
- only make GET requests
- contain zero business logic
- return raw backend response

---

## Example Tools

```
search_buses()
get_timings()
check_availability()
get_ticket_status()
```

Example structure:

```python
def search_buses(params):
    response = requests.get(BACKEND_URL + "/routes", params=params)
    return response.json()
```

Nothing else should exist inside tools.

No:
- validation
- calculations
- data modification
- POST/PUT/DELETE calls

---

# Intent → Tool Mapping

Examples:

| User Message | Tool |
|-------------|-------|
| show buses | search_buses |
| timings | get_timings |
| seats available | check_availability |
| ticket status | get_ticket_status |

Chatbot only fetches and displays data.

---

# Memory Design

Each user has one session:

```
session = {
  history: [],
  state: {}
}
```

history → conversation  
state → temporary info (route, date, etc.)

Purpose:
- follow-up questions
- context awareness

Storage:
- in-memory dict or Redis

Not required:
- vector DB
- embeddings
- RAG

Keep simple.

---

# What Chatbot MUST Do

✅ Answer informational queries  
✅ Extract parameters  
✅ Call GET APIs  
✅ Format results clearly  

---

# What Chatbot MUST NOT Do

❌ Book tickets  
❌ Cancel tickets  
❌ Modify trips  
❌ Update database  
❌ Execute POST/PUT/DELETE  
❌ Contain business logic  
❌ Perform calculations  

If Chatbot performs any action → design is wrong

---

# Mental Model

Streamlit → interaction  
Chatbot → thinking + routing  
Backend → data provider  
Database → storage  
Gemini → reasoning only  

---

# Summary

Chatbot = read-only assistant  
Backend = data source  
Gemini = reasoning engine  
Tools = GET API wrappers only  

The Chatbot is simply a **smart information retrieval layer** for the system.

This architecture is fixed and must not change.
