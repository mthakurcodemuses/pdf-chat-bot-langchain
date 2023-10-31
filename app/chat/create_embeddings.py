from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.chat.vector_store.pinecone_vector_store import pinecone_vector_store


def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    """
    Generate and store embeddings for the given pdf

    1. Extract text from the specified PDF.
    2. Divide the extracted text into manageable chunks.
    3. Generate an embedding for each chunk.
    4. Persist the generated embeddings.

    :param pdf_id: The unique identifier for the PDF.
    :param pdf_path: The file path to the PDF.

    Example Usage:

    create_embeddings_for_pdf('123456', '/path/to/pdf')
    """

    # Instantiate TextSplitter
    pdf_text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    # Instantiate PDFLoader
    pdf_loader = PyPDFLoader(pdf_path)
    print("Loaded the PDF")

    # Split the text into chunks
    split_docs = pdf_loader.load_and_split(pdf_text_splitter)
    print("Finished splitting the docs")

    for doc in split_docs:
        doc.metadata = {
            "page": doc.metadata["page"],
            "pdf_id": pdf_id,
            "text": doc.page_content
        }

    # Add the embeddings to the vector store
    pinecone_vector_store.add_documents(split_docs)
    print("Finished updating the Pinecone vector db with the embeddings")

