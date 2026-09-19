from flashrank import Ranker, RerankRequest


def rerank_documents(query: str, documents, top_k: int = 3):
    """
    Rerank retrieved LangChain documents using FlashRank.
    """

    if not documents:
        return []

    passages = []

    for index, document in enumerate(documents):
        passages.append(
            {
                "id": str(index),
                "text": document.page_content,
                "meta": document.metadata,
            }
        )

    ranker = Ranker()

    rerank_request = RerankRequest(
        query=query,
        passages=passages,
    )

    results = ranker.rerank(rerank_request)

    results = results[:top_k]

    reranked_documents = []

    for result in results:
        document_index = int(result["id"])
        document = documents[document_index]

        document.metadata["rerank_score"] = result["score"]

        reranked_documents.append(document)

    return reranked_documents