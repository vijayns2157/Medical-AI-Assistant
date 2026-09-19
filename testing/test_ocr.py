from pathlib import Path

from pdf2image import convert_from_path
import pytesseract


PDF_PATH = Path("data/documents/CPT 2026.pdf")


def main():
    print("=" * 60)
    print("OCR TEST - PAGE 1")
    print("=" * 60)

    print("Converting page 1 to image...")

    images = convert_from_path(
        PDF_PATH,
        first_page=1,
        last_page=1,
        dpi=200,
    )

    print(f"Image created: {images[0].size}")

    print("Running OCR...")

    text = pytesseract.image_to_string(images[0])

    print("\n" + "-" * 60)
    print("OCR RESULT")
    print("-" * 60)

    print(text[:2000])

    print("\n" + "=" * 60)
    print(f"Characters extracted: {len(text.strip())}")
    print("=" * 60)


if __name__ == "__main__":
    main()