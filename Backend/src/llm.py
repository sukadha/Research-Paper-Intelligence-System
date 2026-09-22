import os

from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# CHECK API KEY
# =========================================================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found.\n"
        "Please add your Gemini API key to the .env file."
    )


# =========================================================
# CREATE GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# GEMINI MODEL
# =========================================================

MODEL_NAME = "gemini-2.5-flash"


# =========================================================
# GENERATE ANSWER
# =========================================================

def generate_answer(question, context):
    """
    Generate an answer using Gemini based only on
    the retrieved research-paper context.

    Parameters:
        question (str):
            User's question.

        context (str):
            Relevant text retrieved from FAISS.

    Returns:
        str:
            Gemini-generated answer.
    """

    prompt = f"""
You are a Research Paper Intelligence Assistant.

Your task is to answer the user's question using
ONLY the research-paper context provided below.

IMPORTANT RULES:

1. Use only information available in the provided context.
2. Do not invent or assume information.
3. Do not use outside knowledge.
4. If the answer cannot be found in the context,
   clearly say that the information was not found
   in the provided research papers.
5. Give a clear and concise answer.
6. If multiple papers provide relevant information,
   combine the information carefully.
7. Do not mention information that is unrelated
   to the user's question.

USER QUESTION:
{question}


RESEARCH PAPER CONTEXT:
{context}


ANSWER:
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response and response.text:

            return response.text.strip()

        return (
            "I could not generate an answer from "
            "the provided research papers."
        )

    except Exception as e:

        return (
            f"Error generating answer with Gemini: {e}"
        )


# =========================================================
# TEST GEMINI CONNECTION
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("GEMINI LLM TEST")
    print("=" * 60)

    test_question = (
        "What is artificial intelligence?"
    )

    test_context = """
Artificial intelligence is a field of computer
science concerned with building intelligent systems.
These systems are designed to perform tasks that
normally require human intelligence.
"""

    print("\nTesting Gemini connection...")

    answer = generate_answer(
        test_question,
        test_context
    )

    print("\nQuestion:")
    print(test_question)

    print("\nAnswer:")
    print(answer)

    print("\n" + "=" * 60)
    print("GEMINI LLM TEST COMPLETED")
    print("=" * 60)