\# QUICKBUS AI SYSTEM SPECIFICATION (FINAL)
Flask + LangChain + HuggingFace Hosted LLM

This document is the SINGLE SOURCE OF TRUTH for the QuickBus AI integration.

All future development and discussions MUST follow this design exactly.

No alternative architectures.

---

# 🎯 Objective

Add AI capabilities to QuickBus with:

1. Chatbot → answers questions (READ ONLY)
2. Agent → performs actions (READ + WRITE)

The existing QuickBus backend remains unchanged.

---

# 🏗 Final Architecture

Frontend (React)
      ↓
AI Server (Python + Flask + LangChain)
      ↓
QuickBus Backend (Node + Express)
      ↓
MongoDB

LLM Provider:
HuggingFace Hosted Models (API based, NOT local)

---

# 🔴 Golden Rules (Always True)

1. AI server NEVER accesses database directly
2. AI server NEVER contains business logic
3. AI server ONLY calls backend APIs
4. Backend handles ALL DB + logic
5. LLM NEVER executes code
6. LLM ONLY returns text/tool decisions
7. Models are hosted on HuggingFace (no local inference)

If any rule is broken → architecture is wrong.

---

# 🧩 Tech Stack

## Backend
- Node
- Express
- MongoDB

## AI Server
- Python
- Flask
- LangChain
- requests/httpx
- HuggingFace Inference API (hosted LLM)

---

# 🧠 Role of Each Component

---

## Frontend
- sends user message
- shows AI response

No logic.

---

## AI Server (Flask + LangChain)

Acts as intelligence + orchestration layer.

Responsibilities:
- receive messages
- call HuggingFace LLM via LangChain
- maintain memory
- select tools
- call backend APIs
- format responses

It behaves like an automated smart client.

It NEVER:
- touches DB
- modifies models
- contains booking logic

---

## Backend (Express)

Acts as execution layer.

Responsibilities:
- booking
- canceling
- validations
- authentication
- DB queries

This is the single source of truth.

ALL real operations happen here.

---

# 🤖 LLM Provider

We use:

HuggingFace hosted LLMs via API

NOT:
- local models
- GPUs
- on-device inference

Flow:

LangChain → HuggingFace API → model → response

The LLM is simply a remote service returning text.

---

# 🤖 Modules

---

## 1️⃣ Chatbot (READ ONLY)

Purpose:
Answer informational queries.

Examples:
- show buses
- availability
- timings
- prices
- ticket status

Allowed:
- GET APIs only

Not allowed:
- booking
- cancel
- update operations

Flow:
User → Chatbot → tool → backend GET → reply

---

## 2️⃣ Agent (READ + WRITE)

Purpose:
Execute tasks.

Examples:
- book ticket
- cancel ticket
- reschedule

Allowed:
- GET + POST + PUT + DELETE

Flow:
User → Agent → tool → backend API → DB change → confirmation

---

# 🔧 LangChain Usage

LangChain is used ONLY for:

- LLM wrapper
- tool calling
- memory
- agent orchestration

LangChain does NOT:
- replace backend
- access DB
- store business logic

It only coordinates thinking + tools.

---

# 🔌 Tools (Backend Wrappers)

Each tool = one backend API call.

Tools are normal Python functions.

Examples:

search_buses()  → GET /routes
book_ticket()   → POST /book
cancel_ticket() → POST /cancel

LangChain Agent automatically selects which tool to execute.

Tools perform HTTP requests to backend.

---

# 💾 Memory Design

Each user has ONE session memory.

Structure:

session = {
  history: [],   # conversation context
  state: {}      # structured data (routeId, seats, etc.)
}

history:
- used by chatbot + agent

state:
- mainly used by agent

Storage:
- in-memory dict OR Redis

No vector DB
No embeddings
No RAG

Simple session memory only.

---

# 🔁 Execution Logic

## Chatbot
message
→ LangChain conversation chain
→ optional tool
→ backend GET
→ formatted answer

---

## Agent
message
→ LangChain Agent
→ chooses tool
→ tool calls backend
→ backend updates DB
→ confirmation

---

# 📁 Project Structure

ai-server/
│
├── app.py
├── routes/
│   ├── chat.py
│   └── agent.py
├── tools/
│   ├── search.py
│   ├── booking.py
│   └── cancel.py
├── services/
│   ├── llm.py          # HuggingFace + LangChain setup
│   ├── memory.py
│   └── backend_client.py
└── requirements.txt

---

# 🧠 Final Mental Model

Frontend → interaction  
AI Server → thinking + orchestration  
Backend → execution  
Database → storage  

HuggingFace LLM → reasoning only  
LangChain → tool management  
Python → API calls  
Backend → real work  

---

# ✅ Final Summary

Chatbot = read-only assistant  
Agent = action executor  
AI server = smart client only  
Backend = real system  
LLM = hosted reasoning engine  

No local models.
No DB access from AI.
No business logic in AI.

This design is final and must not change.
