import sys
import os


# =========================================================
# ADD SRC FOLDER TO PYTHON PATH
# =========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SRC_DIR = os.path.join(
    CURRENT_DIR,
    "src"
)

sys.path.append(SRC_DIR)


# =========================================================
# IMPORT RAG PIPELINE
# =========================================================

from rag_pipeline import rag_pipeline


# =========================================================
# DISPLAY HEADER
# =========================================================

def display_header():

    print("\n" + "=" * 70)
    print("        RESEARCH PAPER INTELLIGENCE SYSTEM")
    print("=" * 70)

    print("\nAsk questions about your uploaded research papers.")

    print(
        "The system searches your research papers, "
        "retrieves relevant sections, and generates "
        "an answer using Gemini."
    )

    print("\nMultiple-paper questions are supported.")

    print("\nExamples:")
    print("  - What dataset was used?")
    print("  - What methodology was used in paper1?")
    print("  - What methodologies were used across the papers?")
    print("  - What were the main results?")
    print("  - What are the limitations of the papers?")

    print("\nType 'exit' to close the application.")

    print("=" * 70)


# =========================================================
# DISPLAY ANSWER AND SOURCES
# =========================================================

def display_result(result):

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)

    print()

    print(result.get(
        "answer",
        "No answer generated."
    ))

    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)

    sources = result.get(
        "sources",
        []
    )

    if sources:

        for source in sources:

            print(
                f"{source['source']} "
                f"— Page {source['page']}"
            )

    else:

        print("No sources found.")

    print("=" * 70)


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    display_header()

    while True:

        # -------------------------------------------------
        # Get user question
        # -------------------------------------------------

        try:

            question = input(
                "\nEnter your question:\n> "
            ).strip()

        except KeyboardInterrupt:

            print(
                "\n\nApplication stopped."
            )

            break

        except EOFError:

            print(
                "\n\nApplication stopped."
            )

            break

        # -------------------------------------------------
        # Check empty question
        # -------------------------------------------------

        if not question:

            print(
                "\nPlease enter a question."
            )

            continue

        # -------------------------------------------------
        # Exit
        # -------------------------------------------------

        if question.lower() in [
            "exit",
            "quit",
            "q"
        ]:

            print(
                "\nThank you for using "
                "Research Paper Intelligence System."
            )

            break

        # -------------------------------------------------
        # Detect multiple-paper question
        # -------------------------------------------------

        multiple_paper_keywords = [
            "across the papers",
            "across all papers",
            "all papers",
            "multiple papers",
            "different papers",
            "papers",
            "compare the papers",
            "compare papers",
            "between the papers"
        ]

        is_multiple_paper_question = any(
            keyword in question.lower()
            for keyword in multiple_paper_keywords
        )

        # -------------------------------------------------
        # Choose number of retrieved chunks
        # -------------------------------------------------

        if is_multiple_paper_question:

            top_k = 12

            print(
                "\nMultiple-paper question detected."
            )

            print(
                "Retrieving relevant information "
                "from across the papers..."
            )

        else:

            top_k = 3

            print(
                "\nSearching for relevant sections..."
            )

        # -------------------------------------------------
        # Run RAG pipeline
        # -------------------------------------------------

        try:

            result = rag_pipeline(
                question,
                top_k=top_k
            )

            # ---------------------------------------------
            # Display result
            # ---------------------------------------------

            if result.get("status") == "success":

                display_result(result)

            else:

                print("\nError:")

                print(
                    result.get(
                        "message",
                        "Unknown error."
                    )
                )

        except Exception as e:

            print(
                "\nAn error occurred while "
                "processing your question:"
            )

            print(e)


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    main()