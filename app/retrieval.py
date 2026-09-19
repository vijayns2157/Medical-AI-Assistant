import re

from langchain_qdrant import QdrantVectorStore

from app.config import QDRANT_URL, QDRANT_COLLECTION
from app.embeddings import get_embeddings


def get_vector_store():
    embeddings = get_embeddings()

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=QDRANT_COLLECTION,
        url=QDRANT_URL,
    )

    return vector_store


def extract_cpt_code(query: str):
    """
    Extract a 5-digit CPT code from the user query.
    Example:
        'What is CPT code 99213?' -> '99213'
    """

    match = re.search(r"\b\d{5}\b", query)

    if match:
        return match.group(0)

    return None


def search_documents(query: str, k: int = 5):
    vector_store = get_vector_store()

    cpt_code = extract_cpt_code(query)

    if cpt_code:
        search_query = cpt_code
    else:
        search_query = query

    results = vector_store.similarity_search_with_score(
        search_query,
        k=k,
    )

    return results