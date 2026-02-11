
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm_summary():
    # low-level endpoint (provider connection)
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",          # IMPORTANT
        huggingfacehub_api_token=os.getenv("HF_TOKEN"),
        temperature=0,
        max_new_tokens=250
    )

    # chat wrapper (what LangChain expects)
    chat_model = ChatHuggingFace(llm=endpoint)

    return chat_model

# def get_llm():
#     return ChatGroq(
#         model="llama-3.1-8b-instant",
#         temperature=0,
#         max_tokens=512,
#         api_key=os.getenv("GROQ_API_KEY")
#     )

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,          # deterministic (important for tools)
        max_output_tokens=512,  # Gemini uses this instead of max_tokens
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )