import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables (MONGO_URI)
load_dotenv()


def run_ingestion():
    # 1. Load the TechForge Price List
    pdf_path = "./data/wellness_industrial equipments.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        return

    print(f"Loading {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # 2. Chunking for Product/Pricing Precision
    # Note: Opted for 500-char chunks to ensure pricing rows aren't split across nodes,
    # balancing LLM context density vs. storage overhead.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(docs)

    # 3. Connect to TypeStream Atlas
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("Error: MONGO_URI environment variable not set.")
        return

    client = MongoClient(mongo_uri)
    collection = client.typestream.techforge_vectors

    # 4. Push to Vector Store
    # In 2026, we include source metadata for better context
    data_to_insert = [
        {
            "text": c.page_content,
            "metadata": {
                **c.metadata,
                "project": "11-techforge-rag",
                "source": "TechForge Price List 05/2026",
                "category": "pricing",
                "timestamp": os.path.getmtime(pdf_path),
            },
        }
        for c in chunks
    ]

    collection.insert_many(data_to_insert)

    print(f"Success: {len(chunks)} chunks ingested to Atlas from {pdf_path}.")


if __name__ == "__main__":
    run_ingestion()
