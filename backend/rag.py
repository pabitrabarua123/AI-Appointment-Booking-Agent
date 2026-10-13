
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

load_dotenv()

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_or_create_collection(
    name="therapy_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def retrieve_context(query: str, top_k: int = 4) -> str:
    """Retrieve the most relevant passages for a user query."""

    if collection.count() == 0:
        return ""

    embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = embedding_response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    print("Retrieved passages:", results["metadatas"])

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    passages = []

    for document, metadata in zip(documents, metadatas):
        source = metadata.get("source", "Unknown document")
        page = metadata.get("page", "Unknown")

        passages.append(
            f"Source: {source}, page: {page}\n{document}"
        )

    return "\n\n---\n\n".join(passages)
