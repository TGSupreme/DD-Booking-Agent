# QuickBus AI Chatbot Module (Read-Only Information Assistant)

---

# Overview

QuickBus AI Chatbot is a **read-only conversational assistant** for the QuickBus Bus Booking System.

It allows users to retrieve **bus and route information using natural language**.

The chatbot only:
- fetches information
- calls backend GET/READ APIs
- formats answers

The chatbot NEVER:
- books tickets
- cancels tickets
- modifies data
- updates database records

It behaves strictly as an **information retrieval layer**.

---

# Final Scope (Locked)

The chatbot supports ONLY:

✅ Search buses  
✅ View routes  
✅ View timings  
✅ Check seat availability  
✅ View prices  
✅ Show available stops/locations  
✅ General Q&A  

The chatbot DOES NOT support:

❌ Ticket booking  
❌ Ticket cancellation  
❌ Ticket status  
❌ Payment  
❌ Any POST/PUT/DELETE business actions  

---

# Goal

Users should be able to ask:

• "Show buses from Surat to Ahmedabad"  
• "Are seats available tomorrow?"  
• "What time does this bus arrive?"  
• "List all stops"  
• "Cheapest bus for today"  

System must:
1. Understand intent
2. Extract parameters
3. Call backend APIs
4. Return clean formatted answers

---

# Core Principle

LLM → reasoning only  
Chatbot → orchestration only  
Backend → data provider only  

The chatbot NEVER contains business logic.

---

# Final Architecture

Streamlit (UI)
      ↓
Chatbot Server (Flask + LangChain + Gemini)
      ↓
Backend APIs (Read-only)
      ↓
Database

---

# Responsibilities

---

## 1. Streamlit (Frontend)

Responsibilities:
- send user messages
- display chatbot responses
- show tables/cards

Rules:
- no API logic
- no business logic
- no database calls

UI only.

---

## 2. AI Chatbot Server (Main Work Area)

Acts as:
Intelligence + routing layer

Responsibilities:
- receive messages
- call Gemini LLM
- detect intent
- extract parameters
- select correct tool
- call backend API
- format responses

Never:
- access DB
- modify data
- perform calculations
- execute business logic

---

## 3. Backend (Black Box)

Acts as:
Single source of truth

Chatbot:
- sends requests
- receives JSON

Chatbot MUST NOT depend on backend internals.

Treat backend as:
Input → Output only.

---

# Golden Rules (Strict)

1. Chatbot NEVER accesses DB
2. Chatbot NEVER contains business logic
3. Chatbot ONLY calls backend APIs
4. Chatbot NEVER modifies data
5. LLM NEVER executes code
6. LLM ONLY returns reasoning/text
7. All models run via cloud APIs only
8. Backend is the only truth

If any rule breaks → architecture is wrong

---

# Tech Stack

Frontend:
- Streamlit

Chatbot Server:
- Python 3.10+
- Flask
- LangChain
- langchain-google-genai
- requests/httpx

LLM Provider:
- Google Gemini (hosted)

---

# LLM Configuration

services/llm.py

```python
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3
    )

# Backend APIs (Official Contracts)

These are the ONLY APIs the chatbot is allowed to use.

Rules:
- Chatbot calls backend only through these APIs
- No direct DB access
- No hidden endpoints
- No internal logic usage
- Backend is treated as a black box

---

## 1. Login

Name: login  
Method: POST  
URL: /api/login  

Purpose:
Authenticate user credentials and create a secure session using JWT stored in an HTTP-only cookie.

Query Params:
None

Body:
{
  email: string (valid email),
  password: string (6+ characters recommended)
}

Response:
{
  success: boolean,
  message: string,
  user: {
    id: string,
    name: string,
    email: string,
    phone: number,
    role: user | admin
  }
}

Cookies Set:
- accesstoken (JWT, HttpOnly, SameSite=Lax, Max-Age=86400)

Notes:
- Only used if backend requires authentication
- Chatbot never stores passwords
- Authentication handled automatically via cookies

---

## 2. Get All Stops

Name: get_all_stops  
Method: GET  
URL: /api/admin/route/stops  

Purpose:
Fetch all available bus stops/locations configured in the system.

Query Params:
None

Body:
None

Response:
{
  success: boolean,
  message: string,
  allstops: string[]
}

Used for:
- "Show all stops"
- autocomplete suggestions
- validating source/destination

---

## 3. Search Bus

Name: search_bus  
Method: POST  
URL: /api/user/search  

Purpose:
Search available buses for a given source, destination, and travel date.

Query Params:
None

Body:
{
  from: string,
  to: string,
  traveldate: YYYY-MM-DD
}

Response:
{
  success: boolean,
  message: string,
  buses: [
    {
      busId: string,
      tripId: string,
      busname: string,
      busnumber: string,
      type: sleeper | seating,
      from: string,
      to: string,
      totaltime: {
        hour: number,
        minute: number
      },
      totalseats: number,
      price: number,
      fromtime: string,
      totime: string,
      days: number[],
      availableseat: number,
      amenties: string[]
    }
  ]
}

Used for:
- searching buses
- checking timings
- seat availability
- pricing info
- amenities
- travel duration

This is the PRIMARY chatbot API.

---

# Tools Design (Critical)

Each tool MUST map 1-to-1 with exactly one backend API.

Definition:
1 tool = 1 API wrapper

Tools must:
- only call backend
- return raw JSON
- contain ZERO business logic

Tools must NOT:
- validate data
- transform results heavily
- calculate anything
- modify state
- call POST/PUT/DELETE business endpoints

---

## Tool List (Final)

```
login()
get_all_stops()
search_bus()
```

These are the ONLY tools allowed.

No extra tools should exist.

---

## Example Tool Implementation

```python
import requests

BACKEND_URL = "http://localhost:2026"

def search_bus(params):
    response = requests.post(
        f"{BACKEND_URL}/api/user/search",
        json=params
    )
    return response.json()
```

Keep tools extremely thin.

---

# Intent → Tool Mapping

Examples:

User: "Show buses from Surat to Ahmedabad"  
→ search_bus

User: "Are seats available tomorrow?"  
→ search_bus

User: "List all stops"  
→ get_all_stops

User: "Login me"  
→ login

All informational queries must resolve using only these tools.

---

# Chatbot Workflow

For every user message:

Step 1 → Receive query  
Step 2 → Send to LLM for reasoning  
Step 3 → Detect intent  
Step 4 → Extract parameters  
Step 5 → Select tool  
Step 6 → Call backend API  
Step 7 → Format response  

Flow:

User  
↓  
LLM reasoning  
↓  
Tool call  
↓  
Backend  
↓  
Formatted answer  

---

# Memory Design

Use simple session memory only.

Structure:

session = {
  history: [],
  state: {}
}

history:
- stores conversation

state:
- temporary parameters (from, to, date)

Purpose:
- follow-up questions
- context awareness

Not required:
- vector database
- embeddings
- RAG

Keep it simple.

---

# What Chatbot MUST Do

✅ Understand intent  
✅ Extract parameters  
✅ Call correct tool  
✅ Fetch backend data  
✅ Format answers clearly  

---

# What Chatbot MUST NOT Do

❌ Book tickets  
❌ Cancel tickets  
❌ Modify database  
❌ Perform calculations  
❌ Execute business logic  
❌ Access DB directly  
❌ Call unauthorized APIs  

If any of these happen → architecture is violated.

---

# Mental Model

Streamlit → UI  
Chatbot → thinking + routing  
Backend → data source  
Database → storage  
Gemini → reasoning engine  

Chatbot = smart information retriever only

---

# Final Summary

QuickBus AI Chatbot is:

✔ Read-only  
✔ Tool-calling  
✔ Stateless  
✔ API-driven  
✔ Information assistant only  

It never performs actions.

Architecture is fixed and must not change.
