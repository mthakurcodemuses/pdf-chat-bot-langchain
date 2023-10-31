from langchain.chat_models import ChatOpenAI


def build_llm(chat_args):
    return ChatOpenAI(streaming=chat_args.streaming, verbose=True)


def build_condense_question_chain_llm(chat_args):
    return ChatOpenAI(streaming=False, verbose=True)
