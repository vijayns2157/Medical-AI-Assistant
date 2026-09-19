from app.retrieval import search_documents


def main():
    query = "What is the place of service code for telehealth?"

    print("=" * 60)
    print("QDRANT RETRIEVAL TEST")
    print("=" * 60)

    results = search_documents(query, k=5)

    print(f"\nQuery: {query}")
    print(f"Results returned: {len(results)}")

    for index, (document, score) in enumerate(results, start=1):
        print("\n" + "-" * 60)
        print(f"Result {index}")
        print(f"Score: {score}")
        print(f"Source: {document.metadata.get('source')}")
        print(f"Page: {document.metadata.get('page_number')}")
        print(
            f"Extraction: "
            f"{document.metadata.get('extraction_method')}"
        )
        print("\nContent:")
        print(document.page_content[:1000])

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()