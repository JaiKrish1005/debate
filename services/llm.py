from langchain_ollama import ChatOllama


_llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
    num_predict=512,
)


def get_llm():
    return _llm
