from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.streamable_chain_mixin import StreamableChainMixin
from app.chat.chains.traceable_chain_mixin import TraceableChainMixin


class StreamingConversationalRetrievalChain(TraceableChainMixin, StreamableChainMixin, ConversationalRetrievalChain):
    pass
