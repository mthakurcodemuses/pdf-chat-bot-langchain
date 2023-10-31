from app.chat.chains.streaming_conversational_retrieval_chain import StreamingConversationalRetrievalChain
from app.chat.models import ChatArgs
from app.chat.vector_store.pinecone_vector_store import build_retriever

from app.chat.memory.sql_memory_history import build_memory
from app.chat.language_models.chatopenai import build_llm
from app.chat.language_models.chatopenai import build_condense_question_chain_llm


def build_chat(chat_args: ChatArgs):
    # Instantiate retriever
    retriever = build_retriever(chat_args)
    llm = build_llm(chat_args)
    condense_question_chain_llm = build_condense_question_chain_llm(chat_args)
    memory = build_memory(chat_args)

    return StreamingConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory,
                                                          condense_question_llm=condense_question_chain_llm, verbose=True)
