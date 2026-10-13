
from pathlib import Path
from dotenv import load_dotenv

import chromadb
from openai import OpenAI
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
CHROMA_DIR = BASE_DIR / "chroma_db"

# --------------------------------
# Load environment variables
# --------------------------------

load_dotenv()

client = OpenAI()

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

# Rebuild the collection each time this script is run.
try:
    chroma_client.delete_collection("therapy_knowledge")
except Exception:
    pass

collection = chroma_client.create_collection(
    name="therapy_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def chunk_text(text: str, chunk_size: int = 180,
               overlap: int = 30) -> list[str]:
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


documents = []
metadatas = []
ids = []

for pdf_path in KNOWLEDGE_DIR.glob("*.pdf"):
    reader = PdfReader(str(pdf_path))

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        for chunk_number, chunk in enumerate(
            chunk_text(text)
        ):
            documents.append(chunk)
            metadatas.append({
                "source": pdf_path.name,
                "page": page_number
            })
            ids.append(
                f"{pdf_path.stem}-p{page_number}-c{chunk_number}"
            )

if not documents:
    raise RuntimeError(
        f"No PDF text found in {KNOWLEDGE_DIR}. "
        "Check that the PDFs exist and contain extractable text."
    )

# Embed chunks in batches.
batch_size = 50

for start in range(0, len(documents), batch_size):
    end = start + batch_size

    batch_documents = documents[start:end]

    embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=batch_documents
    )

    embeddings = [
        item.embedding
        for item in embedding_response.data
    ]

    collection.add(
        ids=ids[start:end],
        documents=batch_documents,
        metadatas=metadatas[start:end],
        embeddings=embeddings
    )

print(f"Indexed {len(documents)} chunks.")
print(f"ChromaDB location: {CHROMA_DIR}")
