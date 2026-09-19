from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

from pdf2image import convert_from_path
import pytesseract

from app.config import QDRANT_URL, QDRANT_COLLECTION
from app.embeddings import get_embeddings


DOCUMENTS_DIR = Path("data/documents")


def extract_text_with_ocr(pdf_path: Path, page_number: int) -> str:
    """
    Convert one PDF page to an image and extract text using Tesseract OCR.
    page_number is 1-based.
    """

    images = convert_from_path(
        pdf_path,
        first_page=page_number,
        last_page=page_number,
        dpi=200,
    )

    if not images:
        return ""

    text = pytesseract.image_to_string(images[0])

    return text.strip()


def load_documents():
    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {DOCUMENTS_DIR}"
        )

    all_documents = []

    for pdf_file in pdf_files:
        print(f"\nLoading: {pdf_file}")

        loader = PyPDFLoader(str(pdf_file))
        pages = loader.load()

        print(f"Loaded {len(pages)} pages from {pdf_file.name}")

        for index, page in enumerate(pages):
            page_number = index + 1

            text = page.page_content.strip()

            if text:
                print(
                    f"Page {page_number}: "
                    f"Text extraction ({len(text)} chars)"
                )
            else:
                print(
                    f"Page {page_number}: "
                    f"No text found - running OCR..."
                )

                text = extract_text_with_ocr(
                    pdf_file,
                    page_number,
                )

                print(
                    f"Page {page_number}: "
                    f"OCR extracted {len(text)} chars"
                )

            if not text:
                print(
                    f"Page {page_number}: "
                    f"WARNING - no text extracted"
                )
                continue

            metadata = dict(page.metadata)

            metadata["source"] = pdf_file.name
            metadata["page_number"] = page_number
            metadata["extraction_method"] = (
                "text" if page.page_content.strip() else "ocr"
            )

            all_documents.append(
                Document(
                    page_content=text,
                    metadata=metadata,
                )
            )

    return all_documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk_{index}"

    return chunks


def store_in_qdrant(chunks):
    embeddings = get_embeddings()

    print("\nCreating Qdrant vector store...")

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=QDRANT_COLLECTION,
    )

    print(
        f"Successfully stored {len(chunks)} chunks in Qdrant"
    )


def main():
    print("=" * 60)
    print("Medical Coding RAG - Document Ingestion")
    print("=" * 60)

    documents = load_documents()

    print(
        f"\nTotal documents/pages with text: "
        f"{len(documents)}"
    )

    chunks = split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    if not chunks:
        raise RuntimeError(
            "No chunks were created. "
            "PDF text extraction and OCR both failed."
        )

    store_in_qdrant(chunks)

    print("\nIngestion completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()