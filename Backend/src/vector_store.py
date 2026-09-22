import os
import sys
import pickle

import faiss
import numpy as np


# ---------------------------------------------------------
# Allow importing files from the src folder
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

sys.path.append(CURRENT_DIR)


from chunking import extract_all_pdfs, create_chunks
from embeddings import generate_embeddings


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

DOCUMENTS_FOLDER = os.path.join(
    PROJECT_ROOT,
    "documents"
)

VECTOR_STORE_FOLDER = os.path.join(
    PROJECT_ROOT,
    "vector_store"
)

FAISS_INDEX_PATH = os.path.join(
    VECTOR_STORE_FOLDER,
    "index.faiss"
)

METADATA_PATH = os.path.join(
    VECTOR_STORE_FOLDER,
    "metadata.pkl"
)


# ---------------------------------------------------------
# Create vector store
# ---------------------------------------------------------

def create_vector_store():

    print("=" * 60)
    print("STEP 7 - FAISS VECTOR STORE")
    print("=" * 60)

    # Create vector_store folder if it doesn't exist
    os.makedirs(
        VECTOR_STORE_FOLDER,
        exist_ok=True
    )

    # -----------------------------------------------------
    # STEP 1: Extract PDF pages
    # -----------------------------------------------------

    print("\n[1/4] Extracting PDF text...")

    documents = extract_all_pdfs(
        DOCUMENTS_FOLDER
    )

    if not documents:
        print("No PDF documents found.")
        return

    print(
        f"Total pages extracted: {len(documents)}"
    )

    # -----------------------------------------------------
    # STEP 2: Create chunks
    # -----------------------------------------------------

    print("\n[2/4] Creating text chunks...")

    chunks = create_chunks(
        documents,
        chunk_size=1000,
        chunk_overlap=200
    )

    if not chunks:
        print("No chunks were created.")
        return

    print(
        f"Total chunks created: {len(chunks)}"
    )

    # -----------------------------------------------------
    # STEP 3: Generate embeddings
    # -----------------------------------------------------

    print("\n[3/4] Generating embeddings...")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    if embeddings.size == 0:
        print("No embeddings were generated.")
        return

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    # Convert to float32 because FAISS expects float32
    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    # -----------------------------------------------------
    # STEP 4: Create FAISS index
    # -----------------------------------------------------

    print("\n[4/4] Creating FAISS index...")

    embedding_dimension = embeddings.shape[1]

    print(
        f"Embedding dimensions: "
        f"{embedding_dimension}"
    )

    # Create FAISS index using L2 distance
    index = faiss.IndexFlatL2(
        embedding_dimension
    )

    # Add all embeddings
    index.add(embeddings)

    print(
        f"Vectors stored in FAISS: "
        f"{index.ntotal}"
    )

    # -----------------------------------------------------
    # Save FAISS index
    # -----------------------------------------------------

    faiss.write_index(
        index,
        FAISS_INDEX_PATH
    )

    print(
        f"\nFAISS index saved to:\n"
        f"{FAISS_INDEX_PATH}"
    )

    # -----------------------------------------------------
    # Save metadata
    # -----------------------------------------------------

    with open(
        METADATA_PATH,
        "wb"
    ) as file:

        pickle.dump(
            chunks,
            file
        )

    print(
        f"\nMetadata saved to:\n"
        f"{METADATA_PATH}"
    )

    # -----------------------------------------------------
    # Final information
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("FAISS VECTOR STORE CREATED SUCCESSFULLY")
    print("=" * 60)

    print(
        f"\nTotal PDFs processed : 4"
    )

    print(
        f"Total pages          : {len(documents)}"
    )

    print(
        f"Total chunks         : {len(chunks)}"
    )

    print(
        f"Embedding dimension  : {embedding_dimension}"
    )

    print(
        f"FAISS vectors        : {index.ntotal}"
    )

    print(
        "\nFiles created:"
    )

    print(
        "1. vector_store/index.faiss"
    )

    print(
        "2. vector_store/metadata.pkl"
    )

    print("\n" + "=" * 60)


# ---------------------------------------------------------
# Run the program
# ---------------------------------------------------------

if __name__ == "__main__":

    create_vector_store()