from sentence_transformers import SentenceTransformer
import numpy as np


# Load the embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


def generate_embeddings(texts):
    """
    Generate embeddings for a list of text chunks.

    Parameters:
        texts: List of text strings

    Returns:
        NumPy array containing embedding vectors
    """

    if not texts:
        return np.array([])

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings


def generate_single_embedding(text):
    """
    Generate an embedding for a single text.
    """

    if not text:
        return np.array([])

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding


if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("STEP 6 - EMBEDDING GENERATION TEST")
    print("=" * 60)

    # Test text chunks
    test_texts = [
        "Artificial intelligence is a field of computer science.",
        "Machine learning allows computers to learn from data.",
        "Deep learning uses neural networks to learn complex patterns."
    ]

    print(f"\nNumber of test texts: {len(test_texts)}")

    # Generate embeddings
    embeddings = generate_embeddings(test_texts)

    print("\nEmbedding generation completed.")

    print(f"Embedding shape: {embeddings.shape}")

    print(f"Number of vectors: {len(embeddings)}")

    print(f"Vector dimensions: {embeddings.shape[1]}")

    print("\nFirst embedding vector:")
    print(embeddings[0])

    print("\nFirst 10 values of the first vector:")
    print(embeddings[0][:10])

    print("\n" + "=" * 60)
    print("STEP 6 TEST COMPLETED")
    print("=" * 60)