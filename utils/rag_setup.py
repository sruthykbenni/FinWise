# utils/rag_setup.py
import faiss
import numpy as np
import streamlit as st
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pdfplumber
import os
import re

EMB_MODEL_NAME = "all-MiniLM-L6-v2"
EMB_DIM = 384
INDEX_PATH = Path("vector_index.faiss")
META_PATH = Path("index_meta.pkl")

class SimpleRAG:
    def __init__(self, emb_model_name=EMB_MODEL_NAME):
        @st.cache_resource(show_spinner=False)
        def get_embedding_model(name=EMB_MODEL_NAME):
            return SentenceTransformer(name)
        self.model = get_embedding_model(emb_model_name)

        self.index = None
        self.meta = []
        if INDEX_PATH.exists() and META_PATH.exists():
            self.load()

    def create_index(self):
        self.index = faiss.IndexFlatL2(EMB_DIM)
        self.meta = []

    def embed_texts(self, texts):
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

    def add_documents(self, texts, metadatas=None):
        if self.index is None:
            self.create_index()
        embs = self.embed_texts(texts)
        self.index.add(embs.astype("float32"))
        start_id = len(self.meta)
        for i, t in enumerate(texts):
            md = metadatas[i] if metadatas else {}
            md.update({"id": start_id + i, "text": t})
            self.meta.append(md)
        self.save()

    def query(self, q, top_k=5):
        if self.index is None or self.index.ntotal == 0:
            return []
        v = self.embed_texts([q]).astype("float32")
        D, I = self.index.search(v, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.meta):
                results.append(self.meta[idx])
        return results

    def save(self):
        faiss.write_index(self.index, str(INDEX_PATH))
        with open(META_PATH, "wb") as f:
            pickle.dump(self.meta, f)

    def load(self):
        self.index = faiss.read_index(str(INDEX_PATH))
        with open(META_PATH, "rb") as f:
            self.meta = pickle.load(f)

    def ingest_folder(self, folder_path, chunk_size=500, overlap=50):
        folder = Path(folder_path)
        text_items, metas = [], []
        for p in folder.glob("**/*"):
            if p.is_file():
                text = ""
                if p.suffix.lower() in [".txt", ".md"]:
                    text = p.read_text(encoding="utf-8", errors="ignore")
                elif p.suffix.lower() == ".pdf":
                    try:
                        with pdfplumber.open(p) as pdf:
                            for page in pdf.pages:
                                text += page.extract_text() or ""
                    except Exception:
                        continue
                else:
                    continue
                chunks = self._chunk_text(text, chunk_size, overlap)
                for c in chunks:
                    text_items.append(c)
                    metas.append({"source": p.name})
        if text_items:
            self.add_documents(text_items, metadatas=metas)
        return len(text_items)

    def ingest_transactions(self, df):
        texts, metas = [], []
        for _, r in df.iterrows():
            desc = str(r.get("Description", ""))
            amt = r.get("Amount", 0)
            cat = r.get("Category", "Uncategorized")
            date = str(r.get("Date", ""))
            text = f"On {date}, you spent ₹{amt:.2f} for {desc}, categorized under {cat}."
            texts.append(text)
            metas.append({"source": "user-transaction"})
        self.add_documents(texts, metadatas=metas)
        return len(texts)

    def _chunk_text(self, text, chunk_size, overlap):
        text = re.sub(r"\s+", " ", text).strip()
        chunks, start = [], 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        return chunks

@st.cache_resource(show_spinner=False)
def get_rag_index():
    """Return cached SimpleRAG instance to reuse embeddings/index."""
    rag = SimpleRAG()
    if rag.index is None:
        rag.create_index()
    return rag
