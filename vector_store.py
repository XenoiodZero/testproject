"""
Vector store for RAG retrieval using FAISS and sentence-transformers.
Handles loading documents, chunking, embedding, indexing, and querying.
"""

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents: list[dict] = []  # stores {"text": ..., "source": ...}

    def load_documents(self, knowledge_dir: str = "knowledge_base"):
        """Load all .txt and .md files from the knowledge base directory."""
        if not os.path.isdir(knowledge_dir):
            print(f"[VectorStore] Knowledge directory '{knowledge_dir}' not found.")
            return

        for filename in os.listdir(knowledge_dir):
            if filename.endswith((".txt", ".md")):
                filepath = os.path.join(knowledge_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                chunks = self._chunk_text(text, chunk_size=500, overlap=50)
                for chunk in chunks:
                    self.documents.append({"text": chunk, "source": filename})

        print(f"[VectorStore] Loaded {len(self.documents)} chunks from {knowledge_dir}")

    def build_index(self):
        """Embed all documents and add them to the FAISS index."""
        if not self.documents:
            print("[VectorStore] No documents to index.")
            return

        texts = [doc["text"] for doc in self.documents]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        embeddings = np.array(embeddings, dtype="float32")
        self.index.add(embeddings)
        print(f"[VectorStore] Indexed {self.index.ntotal} vectors.")

    def query(self, question: str, top_k: int = 3) -> list[dict]:
        """Retrieve the top_k most relevant chunks for a question."""
        if self.index.ntotal == 0:
            return []

        q_embedding = self.model.encode([question])
        q_embedding = np.array(q_embedding, dtype="float32")
        distances, indices = self.index.search(q_embedding, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append({
                    "text": self.documents[idx]["text"],
                    "source": self.documents[idx]["source"],
                    "score": float(distances[0][i]),
                })
        return results

    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        """Split text into overlapping chunks by word count."""
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end])
            if chunk.strip():
                chunks.append(chunk)
            start += chunk_size - overlap
        return chunks
