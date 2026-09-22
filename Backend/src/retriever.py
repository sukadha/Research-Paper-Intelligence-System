import os
import sys
import pickle

import faiss
import numpy as np


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

sys.path.append(CURRENT_DIR)

from embeddings import generate_single_embedding


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
# Load FAISS index and metadata
# ---------------------------------------------------------

def load_vector_store():

    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(
            "FAISS index not found. "
            "Run vector_store.py first."
        )

    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(
            "metadata.pkl not found. "
            "Run vector_store.py first."
        )

    print("Loading FAISS index...")

    index = faiss.read_index(
        FAISS_INDEX_PATH
    )

    print("FAISS index loaded successfully.")

    print("Loading metadata...")

    with open(
        METADATA_PATH,
        "rb"
    ) as file:

        metadata = pickle.load(file)

    print("Metadata loaded successfully.")

    print(
        f"Total vectors: {index.ntotal}"
    )

    print(
        f"Total metadata records: {len(metadata)}"
    )

    return index, metadata


# ---------------------------------------------------------
# Retrieve relevant chunks
# ---------------------------------------------------------

def retrieve_documents(
    question,
    top_k=3
):

    if not question or not question.strip():
        return []

    # Load vector store
    index, metadata = load_vector_store()

    # -----------------------------------------------------
    # Convert question into embedding
    # -----------------------------------------------------

    question_embedding = generate_single_embedding(
        question
    )

    # Convert to float32
    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    # FAISS expects a 2D array
    question_embedding = np.expand_dims(
        question_embedding,
        axis=0
    )

    # -----------------------------------------------------
    # Search FAISS
    # -----------------------------------------------------

    distances, indices = index.search(
        question_embedding,
        top_k
    )

    # -----------------------------------------------------
    # Prepare results
    # -----------------------------------------------------

    results = []

    for rank, (distance, index_id) in enumerate(
        zip(distances[0], indices[0]),
        start=1
    ):

        # Ignore invalid FAISS index
        if index_id == -1:
            continue

        chunk = metadata[index_id]

        result = {
            "rank": rank,
            "distance": float(distance),
            "text": chunk["text"],
            "source": chunk["source"],
            "page": chunk["page"]
        }

        results.append(result)

    return results


# ---------------------------------------------------------
# Display retrieved results
# ---------------------------------------------------------

def display_results(
    question,
    results
):

    print("\n" + "=" * 70)
    print("RETRIEVAL RESULTS")
    print("=" * 70)

    print(f"\nQuestion:")
    print(question)

    print(
        f"\nTop {len(results)} relevant chunks:"
    )

    for result in results:

        print("\n" + "-" * 70)

        print(
            f"Rank   : {result['rank']}"
        )

        print(
            f"Distance: {result['distance']:.4f}"
        )

        print(
            f"Source : {result['source']}"
        )

        print(
            f"Page   : {result['page']}"
        )

        print("\nRelevant text:")

        print(
            result["text"]
        )

    print("\n" + "=" * 70)


# ---------------------------------------------------------
# Test the retriever
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("STEP 8 - RETRIEVER TEST")
    print("=" * 70)

    question = input(
        "\nEnter your question: "
    ).strip()

    if not question:

        print(
            "No question entered."
        )

        sys.exit()

    try:

        results = retrieve_documents(
            question,
            top_k=3
        )

        if results:

            display_results(
                question,
                results
            )

        else:

            print(
                "\nNo relevant documents found."
            )

    except Exception as e:

        print(
            f"\nError during retrieval: {e}"
        )