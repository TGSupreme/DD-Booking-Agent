# QuickBus AI Module

## Overview

QuickBus AI is an **AI assistant layer** built on top of the existing QuickBus Bus Booking System.

It allows users to interact with the system using **natural language** instead of buttons/forms.

Currently:

- Frontend → Streamlit (temporary UI for development/testing)
- Backend → Node + Express (already implemented)
- AI Server → Flask + LangChain + HuggingFace LLM

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

AI never touches database directly.

---

# Current Architecture

```
Streamlit (Frontend UI)
        ↓
AI Server (Flask + LangChain)
        ↓
Express Backend (already built)
        ↓
MongoDB
```

LLM Provider:
HuggingFace Hosted Models (cloud only)

---

# Component Responsibilities

## 1. Streamlit (Frontend – temporary)

Purpose:
Simple testing UI for AI

Responsibilities:
- send user messages
- display AI responses

No business logic  
No DB calls  

Later:
Streamlit can be replaced by React frontend.

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
- store business logic
- execute bookings directly

Think of it as:
Smart automated client

---

## 3. Backend (Node + Express)

Status:
Already implemented

Acts as:
Execution layer (single source of truth)

Responsibilities:
- booking
- cancellation
- validations
- authentication
- DB queries
- all business rules

All real operations happen here.

AI only sends HTTP requests to this backend.

---

# Golden Rules (Must Always Follow)

1. AI server NEVER accesses DB directly
2. AI server NEVER contains business logic
3. AI server ONLY calls backend APIs
4. Backend handles ALL logic and DB work
5. LLM NEVER executes code
6. LLM ONLY returns text/tool decisions
7. Models are hosted on HuggingFace only
8. No local inference or GPUs

If any rule breaks → architecture is wrong

---

# Tech Stack

## Frontend (current)
- Streamlit

## AI Server
- Python 3.10
- Flask
- LangChain
- langchain-huggingface
- requests/httpx

## Backend (already built)
- Node
- Express
- MongoDB

## LLM Provider
- HuggingFace Inference API (hosted)

---

# LLM Configuration (Final Working Setup)

Modern HuggingFace models are conversational only.

Old approach (deprecated):
❌ HuggingFaceHub  
❌ text-generation task  

New required approach:
✅ HuggingFaceEndpoint + ChatHuggingFace  
✅ conversational task  

---

# services/llm.py (Official Code)

```python
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

load_dotenv()

def get_llm():
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.2-3B-Instruct",
        task="conversational",
        huggingfacehub_api_token=os.getenv("HF_TOKEN"),
        temperature=0.3,
        max_new_tokens=200,
    )

    return ChatHuggingFace(llm=endpoint)
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
User → Agent → tool → backend → DB update → confirmation

---

# Tools Design

Each tool = one backend API wrapper

Examples:

search_buses()  → GET /routes  
book_ticket()   → POST /book  
cancel_ticket() → POST /cancel  

Tools only make HTTP requests.  
No business logic allowed.

Later:
Backend API endpoints will be added and mapped to tools.

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

No:
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
LLM → reasoning only  

---

# Summary

Chatbot = read-only assistant  
Agent = action executor  
AI server = smart client only  
Backend = real system  
LLM = hosted reasoning engine  

This architecture is fixed and must not change.
