from app.retrieval import search_documents
from app.reranker import rerank_documents


def main():
    query = "What is the place of service code for telehealth?"

    print("=" * 60)
    print("QDRANT + FLASHRANK TEST")
    print("=" * 60)

    # Step 1: Retrieve from Qdrant
    results = search_documents(query, k=10)

    documents = [document for document, score in results]

    print(f"\nQdrant returned: {len(documents)} documents")

    # Step 2: Rerank using FlashRank
    reranked_documents = rerank_documents(
        query=query,
        documents=documents,
        top_k=3,
    )

    print(
        f"FlashRank returned: "
        f"{len(reranked_documents)} documents"
    )

    # Step 3: Display final results
    for index, document in enumerate(
        reranked_documents,
        start=1,
    ):
        print("\n" + "-" * 60)
        print(f"Final Result {index}")

        print(
            f"Rerank Score: "
            f"{document.metadata.get('rerank_score')}"
        )

        print(
            f"Source: "
            f"{document.metadata.get('source')}"
        )

        print(
            f"Page: "
            f"{document.metadata.get('page_number')}"
        )

        print("\nContent:")
        print(document.page_content[:1000])

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()