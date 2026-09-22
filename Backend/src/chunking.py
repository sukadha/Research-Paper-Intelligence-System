import os
import sys

# Allow Python to import pdf_loader.py from the same src folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_loader import extract_all_pdfs


def split_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Split text into smaller overlapping chunks.

    Parameters:
        text: Original page text
        chunk_size: Maximum number of characters in each chunk
        chunk_overlap: Number of characters shared between chunks

    Returns:
        List of text chunks
    """

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Move forward while keeping overlap
        start = end - chunk_overlap

    return chunks


def create_chunks(documents, chunk_size=1000, chunk_overlap=200):
    """
    Convert extracted PDF pages into smaller chunks.

    Each chunk contains:
        - text
        - source
        - page
    """

    all_chunks = []

    for document in documents:

        text = document["text"]
        source = document["source"]
        page = document["page"]

        page_chunks = split_text(
            text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for chunk in page_chunks:

            all_chunks.append({
                "text": chunk,
                "source": source,
                "page": page
            })

    return all_chunks


if __name__ == "__main__":

    print("=" * 60)
    print("STEP 5 - TEXT CHUNKING")
    print("=" * 60)

    # Extract all PDF pages
    documents = extract_all_pdfs("documents")

    if not documents:
        print("\nNo documents found.")
        sys.exit()

    print(f"\nTotal pages extracted: {len(documents)}")

    # Create chunks
    chunks = create_chunks(
        documents,
        chunk_size=1000,
        chunk_overlap=200
    )

    print(f"Total chunks created: {len(chunks)}")

    print("\n" + "=" * 60)
    print("FIRST 5 CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(chunks[:5], start=1):

        print(f"\nChunk {i}")
        print("-" * 60)

        print(f"Source : {chunk['source']}")
        print(f"Page   : {chunk['page']}")

        print("\nText:")
        print(chunk["text"])

        print("-" * 60)