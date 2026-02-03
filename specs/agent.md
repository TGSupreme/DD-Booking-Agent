# QuickBus AI Agent Module (Action Executor)

## Overview

QuickBus AI Agent is the **action execution layer** of the QuickBus system.

It allows users to perform **real operations using natural language**, such as:

- booking tickets
- cancelling tickets
- updating trips
- managing reservations

The Agent converts user messages into **backend API calls**.

It does NOT contain any business logic or database access.

---

# Goal

Enable users to perform actions like:

"Book 2 seats from Surat to Ahmedabad tomorrow"  
"Cancel my ticket"  
"Reschedule my booking to Friday"

The Agent should:

1. Understand intent
2. Extract parameters
3. Select correct tool
4. Call backend API
5. Return formatted response

---

# Core Principle

LLM → reasoning only  
Agent → orchestration only  
Backend → execution only  

Agent behaves like a **smart automated client**.

It NEVER owns business logic.

---

# Final Architecture

```
Streamlit (UI)
      ↓
AI Agent Server (Flask + LangChain + Gemini)
      ↓
Backend APIs (HTTP only)
```

---

# Responsibilities

## 1. Streamlit (Frontend – Permanent UI)

Responsibilities:
- send user messages
- display responses
- show confirmations/errors

Rules:
- no logic
- no DB calls
- no direct API logic

Only UI.

---

## 2. AI Agent Server (Your Work Area)

Acts as:
Decision + orchestration layer

Responsibilities:
- receive user messages
- call Gemini LLM
- detect intent
- extract parameters
- maintain session state
- select correct tool
- call backend APIs
- format final response

Never:
- access database
- write business rules
- validate bookings
- calculate prices
- implement ticket logic

All such logic belongs to backend only.

---

## 3. Backend (Black Box)

Acts as:
Execution service

Agent only:
- sends HTTP requests
- receives responses

Agent MUST NOT depend on backend internals.

Treat backend as:
Input → Output API system only.

---

# Golden Rules (Strict)

1. Agent NEVER accesses DB
2. Agent NEVER contains business logic
3. Agent ONLY calls backend APIs
4. LLM NEVER executes code
5. LLM ONLY returns reasoning/text
6. All models run via cloud APIs
7. No local inference
8. Backend is the single source of truth

If any rule is broken → architecture is wrong

---

# Tech Stack

## Frontend
- Streamlit

## Agent Server
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
    HumanMessage(content="Book 2 seats tomorrow")
])

print(response.content)
```

Always pass message objects.  
Do NOT pass plain strings.

---

# Agent Workflow

For every message:

Step 1 → Receive user message  
Step 2 → Send to LLM  
Step 3 → Detect intent  
Step 4 → Extract parameters  
Step 5 → Choose tool  
Step 6 → Call backend API  
Step 7 → Return result  

Flow:

```
User
 ↓
LLM reasoning
 ↓
Tool selection
 ↓
Backend API call
 ↓
Confirmation message
```

---

# Tools Design (Critical)

Each tool = exactly one backend API wrapper.

Tools MUST:
- only send HTTP requests
- contain zero business logic
- return raw backend response

---

## Example Tools

```
book_ticket()
cancel_ticket()
update_ticket()
get_ticket_status()
```

Example structure:

```python
def book_ticket(payload):
    response = requests.post(BACKEND_URL + "/book", json=payload)
    return response.json()
```

Nothing else should exist inside tools.

No:
- validation
- price calculations
- rules
- condition logic

Backend handles everything.

---

# Intent → Tool Mapping

LLM decides which tool to call.

Examples:

| User Message | Tool |
|------------|-------|
| book seats | book_ticket |
| cancel ticket | cancel_ticket |
| modify trip | update_ticket |
| check status | get_ticket_status |

Agent only routes requests.

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
state → structured info (routeId, seats, dates, etc.)

Purpose:
- multi-step booking
- remembering previous inputs

Storage:
- in-memory dict or Redis

Not required:
- vector DB
- embeddings
- RAG

Keep simple.

---

# What Agent MUST Do

✅ Understand intent  
✅ Extract entities (date, seats, route, etc.)  
✅ Call correct tool  
✅ Format response  

---

# What Agent MUST NOT Do

❌ Access database  
❌ Write business logic  
❌ Validate rules  
❌ Store permanent data  
❌ Perform calculations  
❌ Execute bookings itself  

If Agent does any of these → design is wrong

---

# Mental Model

Streamlit → interaction  
Agent → thinking + routing  
Backend → execution  
Database → storage  
Gemini → reasoning only  

---

# Summary

Agent = action executor  
Backend = real system  
Gemini = reasoning engine  
Tools = API wrappers only  

The Agent is simply a **smart bridge between user messages and backend APIs**.

This architecture is fixed and must not change.
