from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

PDF_PATH = Path("data/documents/CPT 2026.pdf")


def main():
    print("=" * 60)
    print("PDF TEXT EXTRACTION TEST")
    print("=" * 60)

    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()

    print(f"Total pages: {len(documents)}")

    non_empty_pages = 0

    for index, document in enumerate(documents[:10]):
        text = document.page_content.strip()

        print("\n" + "-" * 60)
        print(f"Page: {index + 1}")
        print(f"Characters: {len(text)}")

        if text:
            non_empty_pages += 1
            print("Extracted text:")
            print(text[:500])
        else:
            print("NO TEXT EXTRACTED")

    print("\n" + "=" * 60)
    print(f"Non-empty pages in first 10: {non_empty_pages}")
    print("=" * 60)


if __name__ == "__main__":
    main()