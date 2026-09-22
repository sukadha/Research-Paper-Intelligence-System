import os
import pymupdf


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF while preserving page numbers.

    Returns:
        List of dictionaries containing:
        - source
        - page
        - text
    """

    documents = []

    pdf_name = os.path.basename(pdf_path)

    try:
        pdf = pymupdf.open(pdf_path)

        print(f"\nReading: {pdf_name}")
        print(f"Total Pages: {len(pdf)}")

        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text("text").strip()

            if text:
                documents.append({
                    "source": pdf_name,
                    "page": page_number,
                    "text": text
                })

                print(
                    f"Page {page_number}: "
                    f"{len(text)} characters extracted"
                )

            else:
                print(
                    f"Page {page_number}: "
                    f"No text found"
                )

        pdf.close()

        return documents

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return []


def extract_all_pdfs(documents_folder="documents"):
    """
    Extract text from all PDF files inside the documents folder.
    """

    all_documents = []

    if not os.path.exists(documents_folder):
        print(f"Documents folder not found: {documents_folder}")
        return []

    pdf_files = [
        file
        for file in os.listdir(documents_folder)
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("No PDF files found.")
        return []

    print(f"\nFound {len(pdf_files)} PDF files.")

    for pdf_file in sorted(pdf_files):

        pdf_path = os.path.join(
            documents_folder,
            pdf_file
        )

        extracted_pages = extract_text_from_pdf(pdf_path)

        all_documents.extend(extracted_pages)

    return all_documents


if __name__ == "__main__":

    documents = extract_all_pdfs()

    print("\n" + "=" * 60)
    print("PDF EXTRACTION COMPLETED")
    print("=" * 60)

    print(f"Total pages extracted: {len(documents)}")

    if documents:

        print("\nFirst extracted page:")
        print("-" * 60)

        print(f"Source : {documents[0]['source']}")
        print(f"Page   : {documents[0]['page']}")

        print("\nText:")
        print(documents[0]["text"][:1000])

        print("-" * 60)