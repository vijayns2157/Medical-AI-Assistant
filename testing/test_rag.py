from app.rag import ask_question


def main():
    question = (
        "What is the place of service code "
        "for telehealth?"
    )

    print("=" * 60)
    print("MEDICAL CODING RAG TEST")
    print("=" * 60)

    print(f"\nQuestion:\n{question}")

    result = ask_question(question)

    print("\n" + "-" * 60)
    print("ANSWER")
    print("-" * 60)

    print(result["answer"])

    print("\n" + "-" * 60)
    print("SOURCES")
    print("-" * 60)

    for source in result["sources"]:
        print(
            f"Source: {source['source']} | "
            f"Page: {source['page']} | "
            f"Score: {source['score']}"
        )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()