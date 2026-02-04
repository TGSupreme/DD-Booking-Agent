
import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

load_dotenv()

def get_llm():
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