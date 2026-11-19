"""
RAG Knowledge Assistant Service
Embeds Indian travel destination documents using Sentence-Transformers,
indexes them with FAISS, and retrieves relevant grounded context for Gemini.
"""
import os
import glob
import logging
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

INDEX_DIR = "rag_knowledge_base/faiss_index"
INDEX_FILE = os.path.join(INDEX_DIR, "destinations.index")
METADATA_FILE = os.path.join(INDEX_DIR, "metadata.pkl")
DOCS_DIR = "rag_knowledge_base/destinations"

_model = None
_index = None
_documents_metadata = None


def get_embedding_model():
    global _model
    if _model is None:
        logger.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def build_or_load_faiss_index():
    global _index, _documents_metadata

    if _index is not None and _documents_metadata is not None:
        return _index, _documents_metadata

    if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
        try:
            logger.info("Loading existing FAISS index from %s", INDEX_FILE)
            _index = faiss.read_index(INDEX_FILE)
            with open(METADATA_FILE, "rb") as f:
                _documents_metadata = pickle.load(f)
            return _index, _documents_metadata
        except Exception as e:
            logger.warning("Failed loading cached FAISS index: %s. Rebuilding...", e)

    # Build fresh FAISS index
    logger.info("Building new FAISS vector index from markdown articles in %s...", DOCS_DIR)
    os.makedirs(INDEX_DIR, exist_ok=True)

    doc_files = glob.glob(os.path.join(DOCS_DIR, "*.md"))
    if not doc_files:
        logger.warning("No markdown documents found in %s", DOCS_DIR)
        # Fallback empty index
        _index = faiss.IndexFlatL2(384)
        _documents_metadata = []
        return _index, _documents_metadata

    chunks = []
    metadata = []
    
    for file_path in doc_files:
        dest_basename = os.path.basename(file_path).replace(".md", "").replace("_", " ").title()
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split into logical sections by Markdown headers (##)
        sections = content.split("## ")
        title_header = sections[0].strip()

        for sec in sections[1:]:
            lines = sec.strip().split("\n")
            section_title = lines[0].strip()
            section_body = "\n".join(lines[1:]).strip()
            chunk_text = f"Destination: {dest_basename}\nSection: {section_title}\n{section_body}"
            
            chunks.append(chunk_text)
            metadata.append({
                "destination": dest_basename,
                "section": section_title,
                "content": chunk_text,
                "source_file": file_path
            })

    embedder = get_embedding_model()
    embeddings = embedder.encode(chunks, convert_to_numpy=True, show_progress_bar=False)
    embeddings = np.array(embeddings, dtype=np.float32)

    # Normalize vectors for cosine similarity inner product
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(embeddings)
    _documents_metadata = metadata

    # Save to disk
    faiss.write_index(_index, INDEX_FILE)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(_documents_metadata, f)

    logger.info("FAISS index built and saved successfully with %d chunks.", len(chunks))
    return _index, _documents_metadata


def retrieve_context(query: str, top_k: int = 4) -> list:
    """
    Given a user query or destination topic, retrieve top-k relevant document chunks.
    """
    index, metadata = build_or_load_faiss_index()
    if not metadata or index.ntotal == 0:
        return []

    embedder = get_embedding_model()
    q_vec = embedder.encode([query], convert_to_numpy=True)
    q_vec = np.array(q_vec, dtype=np.float32)
    faiss.normalize_L2(q_vec)

    distances, indices = index.search(q_vec, min(top_k, len(metadata)))
    
    results = []
    for rank, idx in enumerate(indices[0]):
        if idx != -1 and idx < len(metadata):
            item = metadata[idx].copy()
            item["score"] = float(distances[0][rank])
            results.append(item)
    return results


if __name__ == "__main__":
    idx, meta = build_or_load_faiss_index()
    res = retrieve_context("What are the best outdoor things to do in Manali?", top_k=2)
    for r in res:
        print("MATCH:", r["destination"], "-", r["section"], f"(Score: {r['score']:.4f})")
