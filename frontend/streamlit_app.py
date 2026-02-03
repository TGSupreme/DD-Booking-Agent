import streamlit as st
import requests

AGENT_URL = "http://localhost:8000/chat"

st.title("🚌 QuickBus AI Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message"):
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    st.chat_message("user").write(prompt)

    # Call your backend agent
    res = requests.post(
        AGENT_URL,
        json={
            "user_id": "user1",
            "message": prompt
        }
    )

    reply = res.json()["reply"]

    # Show agent reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    st.chat_message("assistant").write(reply)
