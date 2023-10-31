from langchain.chains import ConversationalRetrievalChain

from app.chat.models import ChatArgs
from app.chat.vector_store.pinecone_vector_store import build_retriever

from app.chat.memory.sql_memory_history import build_memory
from app.chat.language_models.chatopenai import build_llm


def build_chat(chat_args: ChatArgs):
    # Instantiate retriever
    retriever = build_retriever(chat_args)
    llm = build_llm(chat_args)
    memory = build_memory(chat_args)

    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)
