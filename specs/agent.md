# QuickBus AI Agent Module (Action Executor)

=====================================================
SCOPE-LIMITED VERSION (STRICTLY BASED ON AVAILABLE APIs)
=====================================================

This specification defines the FINAL and FIXED scope of the QuickBus AI Agent.

The Agent ONLY performs actions that are supported by existing backend APIs.

If a backend API does not exist → the Agent MUST NOT support that feature.

-----------------------------------------------------

# Overview

QuickBus AI Agent is the **action execution layer** of the QuickBus system.

It converts natural language into backend API calls.

The Agent:
- understands user intent
- extracts parameters
- selects the correct tool
- calls backend APIs
- returns formatted responses

The Agent NEVER:
- accesses database
- implements business logic
- validates tickets
- performs calculations

It is strictly an orchestration layer.

-----------------------------------------------------

# Supported Features (FINAL)

The Agent supports ONLY these actions:

1. Login user
2. View available stops
3. Search buses
4. View booked/available seats
5. Create ticket booking
6. Complete payment

NOT supported:
❌ Cancel ticket
❌ Reschedule ticket
❌ Ticket status lookup
❌ Modify booking
❌ Refunds
❌ Admin operations

If requested, Agent must reply:
"This action is not supported yet."

-----------------------------------------------------

# Final Architecture

Streamlit (UI)
      ↓
AI Agent Server (Flask + LangChain + Gemini)
      ↓
Backend APIs (HTTP only)

-----------------------------------------------------

# Responsibilities

## 1. Frontend — Streamlit

Responsibilities:
- send messages
- show responses
- display lists (buses/seats/tickets)
- show confirmations/errors

Rules:
- no logic
- no API logic
- no database

UI only.

-----------------------------------------------------

## 2. Agent Server (Core Logic Layer)

Built using:
- Python
- Flask
- LangChain
- Google Gemini API

Responsibilities:
- receive user message
- call LLM
- detect intent
- extract parameters
- select tool
- call backend API
- return formatted result

Never:
- business rules
- DB access
- price logic
- seat logic
- ticket validation

-----------------------------------------------------

## 3. Backend (Black Box)

Backend handles:
- authentication
- seat availability
- booking logic
- pricing
- payment
- data storage

Agent treats backend as:

Input → Output only

-----------------------------------------------------

# Golden Rules (STRICT)

1. Agent NEVER accesses DB
2. Agent NEVER contains business logic
3. Agent ONLY calls APIs
4. LLM NEVER executes code
5. Tools = thin HTTP wrappers only
6. Backend = single source of truth

Breaking any rule = wrong architecture

-----------------------------------------------------

# Tech Stack

Frontend:
- Streamlit

Agent Server:
- Python 3.10
- Flask
- LangChain
- requests/httpx

LLM:
- Google Gemini API (cloud hosted only)

-----------------------------------------------------

# LLM Configuration

services/llm.py

```python
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3
    )
```

Always pass message objects (NOT strings).

-----------------------------------------------------

# Agent Workflow

For every message:

1. Receive message
2. Send to LLM
3. Extract intent + parameters (JSON)
4. Select tool
5. Call backend API
6. Return formatted response

Flow:

User
 ↓
LLM reasoning
 ↓
Tool selection
 ↓
Backend API call
 ↓
Response

------------------------------------------------------------

============================================================
8. BACKEND API CONTRACTS (AUTHORITATIVE SECTION)
============================================================

Base URL:
`/api`

These definitions MUST be followed exactly.

------------------------------------------------------------
API 1 — LOGIN
------------------------------------------------------------

POST /api/login

Purpose:
Authenticate user and set JWT cookie.

Request Body:
{
  "email": "user@email.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": "string",
    "name": "string",
    "email": "string",
    "phone": number,
    "role": "user | admin"
  }
}

Tool:
login()

LLM must extract:
- email
- password

------------------------------------------------------------
API 2 — GET ALL STOPS
------------------------------------------------------------

GET /api/admin/route/stops

Purpose:
Fetch all bus stops.

Request:
None

Response:
{
  "success": true,
  "allstops": ["Surat", "Ahmedabad", "Baroda"]
}

Tool:
get_all_stops()

LLM must extract:
None

------------------------------------------------------------
API 3 — SEARCH BUSES
------------------------------------------------------------

POST /api/user/search

Purpose:
Search available buses.

Request Body:
{
  "from": "Surat",
  "to": "Ahmedabad",
  "traveldate": "2026-02-10"
}

Response:
{
  "success": true,
  "buses": [
    {
      "busId": "string",
      "tripId": "string",
      "busname": "Volvo AC",
      "price": 500,
      "availableseat": 12,
      "fromtime": "08:00 AM",
      "totime": "02:00 PM"
    }
  ]
}

Tool:
search_bus()

LLM must extract:
- from
- to
- traveldate

------------------------------------------------------------
API 4 — GET SEATS
------------------------------------------------------------

POST /api/ticket/seat/get

Purpose:
Get booked seats for a trip.

Request Body:
{
  "tripId": "string",
  "from": "Surat",
  "to": "Ahmedabad",
  "traveldate": "2026-02-10"
}

Response:
{
  "success": true,
  "bookedseat": [1, 2, 5, 8]
}

Tool:
get_all_seats()

LLM must extract:
- tripId
- date
- from
- to

------------------------------------------------------------
API 5 — CREATE TICKET
------------------------------------------------------------

POST /api/ticket/

Purpose:
Create booking (payment pending).

Request Body:
{
  "tripId": "string",
  "from": "Surat",
  "to": "Ahmedabad",
  "price": 500,
  "seats": [3,4],
  "passengers": [
    {"name":"Ahemad","age":22,"gender":"M"}
  ],
  "ticketdate": "2026-02-10"
}

Response:
{
  "success": true,
  "ticket": {
    "_id": "ticketId",
    "pnr": "PNR123",
    "status": "booked",
    "paymentstatus": "pending"
  }
}

Tool:
create_ticket()

LLM must extract:
- tripId
- seats
- passengers
- price
- date

------------------------------------------------------------
API 6 — COMPLETE PAYMENT
------------------------------------------------------------

PUT /api/ticket/update/payment/:ticketId

Purpose:
Mark payment completed.

Request Body:
{
  "price": 1000
}

Response:
{
  "success": true,
  "updatedTicket": {
    "paymentstatus": "completed"
  }
}

Tool:
complete_ticket_payment()

LLM must extract:
- ticketId
- price

------------------------------------------------------------


# Tool Design Rules

Each tool:
- calls exactly one API
- contains zero logic
- returns raw JSON

Example:

```python
def search_bus(payload):
    return requests.post(BASE_URL + "/user/search", json=payload).json()
```

Nothing else allowed.

-----------------------------------------------------

# Intent → Tool Mapping

| User Intent | Tool |
|------------|-------------------------|
| login | login |
| show stops | get_all_stops |
| search bus | search_bus |
| show seats | get_all_seats |
| book ticket | create_ticket |
| pay ticket | complete_ticket_payment |

-----------------------------------------------------

# Memory Design

Per-user session:

```
session = {
  history: [],
  state: {}
}
```

Used for:
- remembering route
- storing tripId
- storing seats
- multi-step booking

Storage:
- in-memory or Redis only

No vector DB / no RAG

-----------------------------------------------------

# Mental Model

Streamlit → UI  
Agent → reasoning + routing  
Backend → execution  
Database → storage  
Gemini → reasoning only  

Agent = smart bridge between language and APIs

-----------------------------------------------------

# Final Summary

QuickBus AI Agent is:

- NOT a booking system
- NOT a business logic layer
- NOT a database client

It is ONLY:

Natural Language → API Calls

Scope is permanently limited to available APIs.

Future features require backend endpoints first.
