import streamlit as st
import requests
import uuid

AGENT_URL = "http://localhost:8000/chat"

st.title("🚌 QuickBus AI Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
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

    # ---- LOADING + ERROR HANDLING ----
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                res = requests.post(
                    AGENT_URL,
                    json={
                        "session_id": st.session_state.session_id,
                        "message": prompt
                    }
                )

                # raise exception for 4xx/5xx
                res.raise_for_status()

                reply = res.json()["reply"]

            except requests.exceptions.RequestException:
                reply = "INTERNAL SERVER ERROR"

        st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
