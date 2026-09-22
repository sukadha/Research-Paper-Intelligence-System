import os
import sys


# =========================================================
# PROJECT PATHS
# =========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

# Make sure src folder is available for imports
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)


# =========================================================
# IMPORT RETRIEVER
# =========================================================

from retriever import retrieve_documents


# =========================================================
# IMPORT GEMINI LLM
# =========================================================

from llm import generate_answer


# =========================================================
# BUILD CONTEXT
# =========================================================

def build_context(results):
    """
    Convert retrieved document chunks into
    context that will be sent to Gemini.
    """

    context_parts = []

    for i, result in enumerate(results, start=1):

        context = f"""
SOURCE {i}

Paper: {result['source']}
Page: {result['page']}

Text:
{result['text']}
"""

        context_parts.append(context)

    return "\n".join(context_parts)


# =========================================================
# BUILD SOURCES
# =========================================================

def build_sources(results):
    """
    Create a clean list containing
    source PDF names and page numbers.
    """

    sources = []

    for result in results:

        source_info = {
            "source": result["source"],
            "page": result["page"]
        }

        # Avoid duplicate source + page combinations
        if source_info not in sources:
            sources.append(source_info)

    return sources


# =========================================================
# MAIN RAG PIPELINE
# =========================================================

def rag_pipeline(question, top_k=3):
    """
    Complete RAG pipeline.

    Flow:

    User Question
          ↓
    FAISS Retriever
          ↓
    Relevant PDF Chunks
          ↓
    Context Building
          ↓
    Gemini LLM
          ↓
    Answer + Sources
    """

    # -----------------------------------------------------
    # VALIDATE QUESTION
    # -----------------------------------------------------

    if not question or not question.strip():

        return {
            "status": "error",
            "message": "Question is required.",
            "answer": "",
            "sources": []
        }

    question = question.strip()


    # -----------------------------------------------------
    # START PIPELINE
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("RAG PIPELINE")
    print("=" * 70)

    print("\nQuestion:")
    print(question)


    # =====================================================
    # STEP 1: RETRIEVE RELEVANT DOCUMENTS
    # =====================================================

    print("\n[1/3] Searching FAISS...")

    results = retrieve_documents(
        question,
        top_k=top_k
    )


    # -----------------------------------------------------
    # NO RESULTS
    # -----------------------------------------------------

    if not results:

        print(
            "\nNo relevant information found."
        )

        return {
            "status": "success",
            "message": "No relevant information found.",
            "answer": (
                "I could not find relevant information "
                "in the uploaded research papers."
            ),
            "sources": []
        }


    print(
        f"Retrieved {len(results)} relevant chunks."
    )


    # =====================================================
    # STEP 2: BUILD CONTEXT
    # =====================================================

    print("\n[2/3] Building context...")

    context = build_context(results)


    # =====================================================
    # STEP 3: SEND TO GEMINI
    # =====================================================

    print(
        "\n[3/3] Generating answer with Gemini..."
    )

    answer = generate_answer(
        question,
        context
    )


    # =====================================================
    # BUILD SOURCES
    # =====================================================

    sources = build_sources(results)


    # =====================================================
    # FINAL RESULT
    # =====================================================

    result = {
        "status": "success",
        "question": question,
        "answer": answer,
        "sources": sources
    }


    return result


# =========================================================
# DISPLAY FINAL ANSWER
# =========================================================

def display_answer(result):

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)


    # -----------------------------------------------------
    # QUESTION
    # -----------------------------------------------------

    print("\nQuestion:")
    print(result.get("question", ""))


    # -----------------------------------------------------
    # ANSWER
    # -----------------------------------------------------

    print("\nAnswer:")
    print(result.get("answer", ""))


    # -----------------------------------------------------
    # SOURCES
    # -----------------------------------------------------

    print("\nSources:")

    sources = result.get("sources", [])

    if sources:

        for source in sources:

            print(
                f"- {source['source']} "
                f"(Page {source['page']})"
            )

    else:

        print("No sources found.")


    print("\n" + "=" * 70)


# =========================================================
# COMMAND LINE TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RESEARCH PAPER INTELLIGENCE SYSTEM")
    print("=" * 70)

    print(
        "\nAsk a question about your research papers."
    )

    print(
        "Type 'exit' to stop."
    )


    # -----------------------------------------------------
    # CONTINUOUS QUESTION LOOP
    # -----------------------------------------------------

    while True:

        question = input(
            "\nEnter your question: "
        ).strip()


        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------

        if question.lower() == "exit":

            print("\nExiting...")

            break


        # -------------------------------------------------
        # EMPTY QUESTION
        # -------------------------------------------------

        if not question:

            print(
                "Please enter a question."
            )

            continue


        # -------------------------------------------------
        # RUN RAG
        # -------------------------------------------------

        try:

            result = rag_pipeline(
                question,
                top_k=3
            )


            # -------------------------------------------------
            # DISPLAY RESULT
            # -------------------------------------------------

            if result["status"] == "success":

                display_answer(result)

            else:

                print(
                    f"\nError: {result.get('message', 'Unknown error')}"
                )


        except Exception as e:

            print(
                f"\nError in RAG pipeline: {e}"
            )