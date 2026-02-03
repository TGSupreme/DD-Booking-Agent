import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm():

    chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

    return chat_model
