from langchain.memory import ConversationBufferWindowMemory
from app.chat.memory.sql_memory_history import SqlMessageHistory

def window__buffer_memory_builder(chat_args):
    return ConversationBufferWindowMemory(
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        return_messages=True,
        memory_key="chat_history",
        output_key="answer",
        k=2
    )