from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys


# =========================================================
# PROJECT PATHS
# =========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SRC_DIR = os.path.join(
    CURRENT_DIR,
    "src"
)

# Add src folder to Python path
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)


# =========================================================
# CONNECT FLASK TO RAG PIPELINE
# =========================================================

from rag_pipeline import rag_pipeline


# =========================================================
# CREATE FLASK APP
# =========================================================

app = Flask(__name__)

# Allow frontend requests
CORS(app)


# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "success",
        "message": "Research Paper Intelligence System API is running.",
        "service": "RAG + FAISS + Gemini"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "Backend is healthy."
    })


# =========================================================
# ASK QUESTION
# =========================================================
#
# GET:
# http://127.0.0.1:5000/api/ask?question=What%20is%20AI?
#
# POST:
# http://127.0.0.1:5000/api/ask
#
# JSON:
# {
#     "question": "What is AI?"
# }
#
# =========================================================

@app.route("/api/ask", methods=["GET", "POST"])
def ask_question():

    try:

        # =================================================
        # GET REQUEST
        # =================================================

        if request.method == "GET":

            question = request.args.get(
                "question",
                ""
            ).strip()


        # =================================================
        # POST REQUEST
        # =================================================

        else:

            data = request.get_json(
                silent=True
            )

            if not data:

                return jsonify({
                    "status": "error",
                    "message": "Request body must contain JSON."
                }), 400


            question = data.get(
                "question",
                ""
            ).strip()


        # =================================================
        # CHECK QUESTION
        # =================================================

        if not question:

            return jsonify({
                "status": "error",
                "message": "Question is required.",
                "example": "/api/ask?question=What%20is%20artificial%20intelligence?"
            }), 400


        # =================================================
        # PRINT REQUEST
        # =================================================

        print("\n" + "=" * 70)
        print("FLASK API REQUEST")
        print("=" * 70)

        print("\nQuestion:")
        print(question)


        # =================================================
        # MULTIPLE PAPER QUESTION DETECTION
        # =================================================

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


        # =================================================
        # SELECT TOP K
        # =================================================

        if is_multiple_paper_question:

            top_k = 12

            print(
                "\nMultiple-paper question detected."
            )

            print(
                "Retrieving information from multiple papers..."
            )

        else:

            top_k = 3

            print(
                "\nNormal question detected."
            )

            print(
                "Retrieving top 3 relevant chunks..."
            )


        # =================================================
        # CALL RAG PIPELINE
        # =================================================

        print(
            "\nConnecting Flask to RAG pipeline..."
        )

        result = rag_pipeline(
            question,
            top_k=top_k
        )


        # =================================================
        # PRINT RESULT STATUS
        # =================================================

        print(
            "\nRAG pipeline completed."
        )

        print(
            f"Status: {result.get('status', 'unknown')}"
        )

        print("=" * 70)


        # =================================================
        # RETURN JSON RESPONSE
        # =================================================

        return jsonify(result), 200


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        print(
            f"\nError in /api/ask: {e}"
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =========================================================
# RUN FLASK SERVER
# =========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RESEARCH PAPER INTELLIGENCE SYSTEM")
    print("=" * 70)

    print("\nStarting Flask backend...")

    print("\nArchitecture:")
    print("Flask")
    print("  ↓")
    print("RAG Pipeline")
    print("  ↓")
    print("FAISS Retriever")
    print("  ↓")
    print("Gemini LLM")
    print("  ↓")
    print("Answer + Sources")


    print("\nAPI:")
    print("http://127.0.0.1:5000")


    print("\nHome:")
    print("GET  http://127.0.0.1:5000/")


    print("\nHealth:")
    print("GET  http://127.0.0.1:5000/api/health")


    print("\nAsk Question:")
    print("GET  http://127.0.0.1:5000/api/ask?question=What%20is%20AI?")


    print("\nAsk Question:")
    print("POST http://127.0.0.1:5000/api/ask")


    print("=" * 70)


    # =====================================================
    # START SERVER
    # =====================================================

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )