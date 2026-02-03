import streamlit as st
import requests

AGENT_URL = "http://localhost:8000/chat"

st.title("QuickBus AI Agent")

user_input = st.text_input("Message")

if st.button("Send"):
    res = requests.post(
        AGENT_URL,
        json={
            "user_id": "user1",
            "message": user_input
        }
    )
    st.write(res.json())
