from app.retrieval import search_documents


def main():
    results = search_documents("99213", k=10)

    for index, (document, score) in enumerate(results, start=1):
        print("\n" + "=" * 80)
        print(f"RESULT {index}")
        print(f"PAGE: {document.metadata.get('page_number')}")
        print(f"SCORE: {float(score):.4f}")
        print("=" * 80)
        print(document.page_content[:1000])


if __name__ == "__main__":
    main()