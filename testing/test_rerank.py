from app.retrieval import search_documents
from app.reranker import rerank_documents


results = search_documents("99213", k=10)

documents = [document for document, score in results]

reranked = rerank_documents(
    query="99213",
    documents=documents,
    top_k=10,
)

for index, document in enumerate(reranked, start=1):
    print("\n" + "=" * 80)
    print(f"RESULT {index}")
    print(f"PAGE: {document.metadata.get('page_number')}")
    print(f"RERANK SCORE: {float(document.metadata.get('rerank_score', 0)):.4f}")
    print("=" * 80)
    print(document.page_content[:500])