import { useRef, useState } from "react";

import {
  Bot,
  CheckCircle2,
  ChevronDown,
  FileText,
  Paperclip,
  Send,
  Sparkles,
  Trash2,
  Upload,
  User,
  X
} from "lucide-react";

import "./App.css";


const API_URL = "http://127.0.0.1:5000";


function App() {

  // =====================================================
  // STATE
  // =====================================================

  const [files, setFiles] = useState([]);

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text:
        "👋 Hi! I’m your Research Paper Assistant.",
      description:
        "You can ask me questions about your uploaded papers, for example:",
      examples: [
        "Summarize a paper",
        "Explain a difficult section",
        "Compare two papers",
        "Extract methodology, datasets and results",
        "Find research gaps",
        "Get answers with source references"
      ],
      time: getCurrentTime()
    }
  ]);

  const [loading, setLoading] = useState(false);

  const [backendStatus, setBackendStatus] = useState("Ready");

  const fileInputRef = useRef(null);


  // =====================================================
  // CURRENT TIME
  // =====================================================

  function getCurrentTime() {

    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit"
    });

  }


  // =====================================================
  // FILE SELECTION
  // =====================================================

  function handleFileChange(event) {

    const selectedFiles = Array.from(
      event.target.files || []
    );

    const pdfFiles = selectedFiles.filter(
      (file) =>
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf")
    );

    setFiles((previousFiles) => {

      const existingNames = new Set(
        previousFiles.map((file) => file.name)
      );

      const newFiles = pdfFiles.filter(
        (file) => !existingNames.has(file.name)
      );

      return [
        ...previousFiles,
        ...newFiles
      ];

    });


    // Reset input
    event.target.value = "";

  }


  // =====================================================
  // REMOVE FILE
  // =====================================================

  function removeFile(fileName) {

    setFiles((previousFiles) =>
      previousFiles.filter(
        (file) => file.name !== fileName
      )
    );

  }


  // =====================================================
  // OPEN FILE SELECTOR
  // =====================================================

  function openFileSelector() {

    if (fileInputRef.current) {

      fileInputRef.current.click();

    }

  }


  // =====================================================
  // SEND QUESTION
  // =====================================================

  async function sendQuestion() {

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }


    // ---------------------------------------------------
    // Add user message
    // ---------------------------------------------------

    const userMessage = {
      id: Date.now(),
      type: "user",
      text: trimmedQuestion,
      time: getCurrentTime()
    };


    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage
    ]);


    setQuestion("");

    setLoading(true);

    setBackendStatus("Thinking...");


    try {

      // =================================================
      // SEND TO FLASK
      // =================================================

      const response = await fetch(
        `${API_URL}/api/ask`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            question: trimmedQuestion
          })
        }
      );


      const data = await response.json();


      // =================================================
      // ERROR RESPONSE
      // =================================================

      if (!response.ok) {

        throw new Error(
          data.message ||
          "Something went wrong."
        );

      }


      // =================================================
      // BOT MESSAGE
      // =================================================

      const botMessage = {
        id: Date.now() + 1,
        type: "bot",
        text: data.answer || "No answer received.",
        sources: data.sources || [],
        time: getCurrentTime()
      };


      setMessages((previousMessages) => [
        ...previousMessages,
        botMessage
      ]);


      setBackendStatus("Ready");


    } catch (error) {

      console.error(
        "API Error:",
        error
      );


      const errorMessage = {
        id: Date.now() + 1,
        type: "bot",
        text:
          "Sorry, I could not connect to the Research Paper backend.",
        errorDetails:
          error.message,
        time: getCurrentTime()
      };


      setMessages((previousMessages) => [
        ...previousMessages,
        errorMessage
      ]);


      setBackendStatus("Backend unavailable");

    } finally {

      setLoading(false);

    }

  }


  // =====================================================
  // ENTER KEY
  // =====================================================

  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      sendQuestion();

    }

  }


  // =====================================================
  // CLEAR CHAT
  // =====================================================

  function clearChat() {

    setMessages([
      {
        id: Date.now(),
        type: "bot",
        text:
          "👋 Hi! I’m your Research Paper Assistant.",
        description:
          "You can ask me questions about your uploaded papers, for example:",
        examples: [
          "Summarize a paper",
          "Explain a difficult section",
          "Compare two papers",
          "Extract methodology, datasets and results",
          "Find research gaps",
          "Get answers with source references"
        ],
        time: getCurrentTime()
      }
    ]);

  }


  // =====================================================
  // FORMAT FILE SIZE
  // =====================================================

  function formatFileSize(bytes) {

    if (!bytes) {
      return "0 KB";
    }

    const mb = bytes / (
      1024 * 1024
    );

    if (mb >= 1) {

      return `${mb.toFixed(1)} MB`;

    }

    return `${Math.max(
      1,
      Math.round(bytes / 1024)
    )} KB`;

  }


  // =====================================================
  // RENDER
  // =====================================================

  return (

    <div className="app">

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="top-header">

        <div className="brand-area">

          <div className="brand-icon">

            <FileText size={36} strokeWidth={2} />

            <div className="search-icon">
              <Sparkles size={13} />
            </div>

          </div>


          <div>

            <h1>
              Research Paper{" "}
              <span>Intelligence System</span>
            </h1>

            <p>
              Upload research papers and get intelligent
              answers using RAG + LLM + GenAI
            </p>

          </div>

        </div>


        <div className="header-right">

          <div className="technology-badge">

            <Sparkles size={17} />

            RAG + LLM + GenAI

          </div>

          <div className="tagline">

            “Your Research, Smarter Answers”

          </div>

        </div>

      </header>


      {/* =================================================
          MAIN CONTENT
      ================================================= */}

      <main className="main-container">


        {/* ===============================================
            LEFT PANEL
        =============================================== */}

        <section className="upload-panel">


          {/* ---------------------------------------------
              UPLOAD HEADER
          --------------------------------------------- */}

          <div className="section-title">

            <div className="section-icon">
              <Upload size={28} />
            </div>

            <h2>
              Upload Research Papers
            </h2>

          </div>


          <p className="section-description">

            Upload one or multiple PDF files to ask
            questions, summarize, compare and more.

          </p>


          {/* ---------------------------------------------
              FILE DROP AREA
          --------------------------------------------- */}

          <div
            className="drop-zone"
            onClick={openFileSelector}
          >

            <div className="cloud-icon">

              <Upload
                size={52}
                strokeWidth={1.8}
              />

            </div>


            <h3>
              Drag & drop PDF files here
            </h3>


            <p>
              or
            </p>


            <button
              className="choose-button"
              onClick={(event) => {

                event.stopPropagation();

                openFileSelector();

              }}
            >

              <FileText size={20} />

              Choose PDF Files

            </button>


            <span className="support-text">

              Supports multiple PDFs

            </span>


            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,application/pdf"
              multiple
              hidden
              onChange={handleFileChange}
            />

          </div>


          {/* ---------------------------------------------
              UPLOADED PAPERS
          --------------------------------------------- */}

          <div className="uploaded-section">

            <div className="uploaded-title-row">

              <h2>
                Uploaded Papers
              </h2>

              {files.length > 0 && (

                <span className="file-count">
                  {files.length}
                </span>

              )}

            </div>


            {files.length === 0 ? (

              <div className="empty-files">

                <FileText size={24} />

                <span>
                  No PDF files selected
                </span>

              </div>

            ) : (

              <div className="file-list">

                {files.map((file) => (

                  <div
                    className="file-card"
                    key={file.name}
                  >

                    <div className="pdf-icon">
                      <FileText size={22} />
                    </div>


                    <div className="file-info">

                      <div className="file-name">
                        {file.name}
                      </div>

                      <div className="file-size">
                        {formatFileSize(file.size)}
                      </div>

                    </div>


                    <button
                      className="remove-file"
                      onClick={() =>
                        removeFile(file.name)
                      }
                      title="Remove file"
                    >

                      <X size={20} />

                    </button>

                  </div>

                ))}

              </div>

            )}

          </div>


          {/* ---------------------------------------------
              BACKEND INFO
          --------------------------------------------- */}

          <div className="backend-info">

            <div className="backend-dot"></div>

            <div>

              <strong>
                RAG Backend Connected
              </strong>

              <span>
                Flask • FAISS • Gemini
              </span>

            </div>

          </div>

        </section>


        {/* ===============================================
            RIGHT CHAT PANEL
        =============================================== */}

        <section className="chat-panel">


          {/* ---------------------------------------------
              CHAT HEADER
          --------------------------------------------- */}

          <div className="chat-header">

            <div className="assistant-info">

              <div className="robot-avatar">

                <Bot
                  size={29}
                  strokeWidth={2}
                />

              </div>


              <div>

                <h2>
                  Research Assistant
                </h2>

                <p>
                  Ask questions, summarize,
                  compare papers and more.
                </p>

              </div>

            </div>


            <div className="ready-status">

              <CheckCircle2 size={17} />

              {backendStatus}

            </div>

          </div>


          {/* ---------------------------------------------
              CHAT BODY
          --------------------------------------------- */}

          <div className="chat-body">

            {messages.map((message) => (

              <div
                key={message.id}
                className={`message-row ${
                  message.type === "user"
                    ? "user-row"
                    : "bot-row"
                }`}
              >

                {/* BOT AVATAR */}

                {message.type === "bot" && (

                  <div className="message-avatar bot-avatar">

                    <Bot size={21} />

                  </div>

                )}


                {/* MESSAGE */}

                <div
                  className={`message-content ${
                    message.type === "user"
                      ? "user-content"
                      : "bot-content"
                  }`}
                >

                  <div className="message-bubble">

                    <p className="message-text">
                      {message.text}
                    </p>


                    {/* INTRODUCTION EXAMPLES */}

                    {message.examples && (

                      <>

                        <p className="intro-description">

                          {message.description}

                        </p>


                        <ul className="example-list">

                          {message.examples.map(
                            (example) => (

                              <li key={example}>
                                {example}
                              </li>

                            )
                          )}

                        </ul>


                        <p className="start-message">

                          Upload your PDF(s) and
                          start asking!

                        </p>

                      </>

                    )}


                    {/* ERROR */}

                    {message.errorDetails && (

                      <div className="error-details">

                        {message.errorDetails}

                      </div>

                    )}


                    {/* SOURCES */}

                    {message.sources &&
                      message.sources.length > 0 && (

                      <div className="sources-box">

                        <div className="sources-title">

                          <FileText size={17} />

                          Sources

                        </div>


                        <div className="sources-list">

                          {message.sources.map(
                            (source, index) => (

                              <div
                                className="source-item"
                                key={`${source.source}-${source.page}-${index}`}
                              >

                                <span className="source-number">
                                  {index + 1}
                                </span>

                                <span>

                                  {source.source}

                                  {" "}

                                  <strong>
                                    (Page {source.page})
                                  </strong>

                                </span>

                              </div>

                            )
                          )}

                        </div>

                      </div>

                    )}

                  </div>


                  <div className="message-time">

                    {message.time}

                  </div>

                </div>


                {/* USER AVATAR */}

                {message.type === "user" && (

                  <div className="message-avatar user-avatar">

                    <User size={20} />

                  </div>

                )}

              </div>

            ))}


            {/* -------------------------------------------
                LOADING
            ------------------------------------------- */}

            {loading && (

              <div className="message-row bot-row">

                <div className="message-avatar bot-avatar">

                  <Bot size={21} />

                </div>


                <div className="message-content bot-content">

                  <div className="message-bubble loading-bubble">

                    <div className="typing">

                      <span></span>
                      <span></span>
                      <span></span>

                    </div>

                    <span>
                      Searching your research papers...
                    </span>

                  </div>

                </div>

              </div>

            )}

          </div>


          {/* ---------------------------------------------
              CHAT INPUT
          --------------------------------------------- */}

          <div className="chat-input-area">

            <div className="input-wrapper">

              <Paperclip
                className="input-paperclip"
                size={23}
              />


              <textarea
                value={question}
                onChange={(event) =>
                  setQuestion(event.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder="Ask a question about your papers..."
                rows={1}
                disabled={loading}
              />


              <button
                className="send-button"
                onClick={sendQuestion}
                disabled={
                  !question.trim() ||
                  loading
                }
                title="Send question"
              >

                <Send size={23} />

              </button>

            </div>


            <div className="input-hint">

              Press Enter to send • Shift + Enter
              for a new line

              <button
                className="clear-button"
                onClick={clearChat}
              >

                <Trash2 size={14} />

                Clear chat

              </button>

            </div>

          </div>

        </section>

      </main>


      {/* =================================================
          FOOTER
      ================================================= */}

      <footer className="footer">

        <span>
          Research Paper Intelligence System
        </span>

        <span>
          RAG + FAISS + Gemini
        </span>

      </footer>

    </div>

  );
}


export default App;