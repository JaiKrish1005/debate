import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

_llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0,
    num_predict=512,
)


def get_llm():
    return _llm
