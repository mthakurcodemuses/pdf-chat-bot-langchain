from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.streamable_chain_mixin import StreamableChainMixin


class StreamingConversationalRetrievalChain(StreamableChainMixin, ConversationalRetrievalChain):
    pass
