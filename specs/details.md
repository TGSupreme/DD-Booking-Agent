# QuickBus AI Module

## Overview

QuickBus AI is an **AI assistant layer** built on top of the existing QuickBus Bus Booking System.

It allows users to interact with the system using **natural language** instead of traditional buttons and forms.

Users can chat with the assistant to search buses, check availability, book tickets, and cancel tickets.

---

# Goal

Enable users to:

- ask bus information
- check availability
- search routes
- book tickets
- cancel tickets

Using simple messages like:

"Show buses from Surat to Ahmedabad"  
"Book 2 seats for tomorrow"  
"Cancel my ticket"

---

# Core Idea

AI handles thinking  
Backend handles execution  

AI NEVER performs business logic or database operations.

AI behaves like a **smart automated client** that only calls APIs.

---

# Final Architecture

```
Streamlit (Frontend UI)
        ↓
AI Server (Flask + LangChain + Gemini)
        ↓
Backend APIs (HTTP only)
```

---

# Component Responsibilities

## 1. Streamlit (Frontend – Permanent)

Purpose:  
Permanent user interface for the system.

Responsibilities:
- send user messages
- display AI responses
- show results (buses, tickets, confirmations)

Rules:
- No business logic
- No database calls
- No direct backend logic

Streamlit is the **official production UI** (not temporary).

---

## 2. AI Server (Python + Flask + LangChain)

Acts as:  
Intelligence + orchestration layer

Responsibilities:
- receive messages
- call LLM
- maintain session memory
- decide which tool to use
- call backend APIs
- format responses

Never:
- access database
- implement business rules
- perform bookings directly

Think of it as:
Smart automated client

---

## 3. Backend (Black Box)

Acts as:
Execution layer

Responsibilities:
- process all requests
- handle validations
- manage authentication
- perform bookings/cancellations
- store and retrieve data

Important:
AI server **must not know or depend on backend internals**.  
It only communicates via HTTP APIs.

---

# Golden Rules (Must Always Follow)

1. AI server NEVER accesses DB directly
2. AI server NEVER contains business logic
3. AI server ONLY calls backend APIs
4. Backend handles ALL real operations
5. LLM NEVER executes code
6. LLM ONLY returns reasoning/text/tool decisions
7. All models run via cloud APIs only
8. No local inference or GPUs

If any rule breaks → architecture is wrong

---

# Tech Stack

## Frontend
- Streamlit

## AI Server
- Python 3.10
- Flask
- LangChain
- langchain-google-genai
- requests / httpx

## Backend
- External HTTP API service (already implemented)

## LLM Provider
- Google Gemini API (hosted)

---

# LLM Configuration (Official Setup)

We use **Google Gemini models** via LangChain.

Old (removed):
❌ HuggingFace  
❌ Local models  

New (final):
✅ Gemini API  
✅ ChatGoogleGenerativeAI  

---

# services/llm.py (Official Code)

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

# How to Call the LLM

```python
from langchain_core.messages import HumanMessage

response = llm.invoke([
    HumanMessage(content="Hello")
])

print(response.content)
```

Do NOT pass plain strings.

Always pass message objects.

---

# Modules

## Chatbot (Read Only)

Purpose:
Answer informational queries

Allowed:
- GET APIs only

Examples:
- show buses
- timings
- availability
- ticket status

Flow:
User → Chatbot → backend GET → response

---

## Agent (Read + Write)

Purpose:
Execute actions

Allowed:
- GET + POST + PUT + DELETE

Examples:
- book ticket
- cancel ticket
- reschedule

Flow:
User → Agent → tool → backend → confirmation

---

# Tools Design

Each tool = one backend API wrapper

Examples:

search_buses()  
book_ticket()  
cancel_ticket()  

Rules:
- tools only make HTTP requests
- no business logic
- no DB access
- no validations

Backend remains the single source of truth.

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
state → structured info (routeId, seats, etc.)

Storage:
- in-memory dict or Redis

Not required:
- vector DB
- embeddings
- RAG

Keep simple.

---

# Mental Model

Streamlit → interaction  
AI Server → thinking  
Backend → execution  
Database → storage  
Gemini → reasoning only  

---

# Summary

Chatbot = read-only assistant  
Agent = action executor  
AI server = smart client only  
Backend = real system  
Gemini = hosted reasoning engine  

This architecture is **final and fixed**.
