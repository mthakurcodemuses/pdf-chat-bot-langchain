from functools import partial
from .pinecone_vector_store import build_retriever

retriever_map = {
    "pinecone_1": partial(build_retriever, doc_search_limit=1),
    "pinecone_2": partial(build_retriever, doc_search_limit=2),
    "pinecone_3": partial(build_retriever, doc_search_limit=3)
}
