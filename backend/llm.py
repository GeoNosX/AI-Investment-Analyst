import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()


llm = ChatOpenAI(
    model="meta/llama-3.1-70b-instruct", 
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1")

