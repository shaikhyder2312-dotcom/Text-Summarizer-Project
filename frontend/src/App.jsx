import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [selectedType, setSelectedType] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!text.trim()) return;

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/summarize",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: text,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to summarize text");
      }

      const data = await response.json();

      setResult(data);
      setSelectedType(null);

    } catch (error) {
      console.error("Error:", error);

      alert(
        "Unable to connect to the summarization API."
      );

    } finally {
      setLoading(false);
    }
  };

  const handleNewText = () => {
    setText("");
    setResult(null);
    setSelectedType(null);
  };

  const handleCopy = (content) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <div className="app">

      {/* ================= HEADER ================= */}

      <header className="header">

        <div className="logo">
          <span className="logo-icon">✦</span>
          TextSummarizer
        </div>

        <div className="api-status">
          <span className="status-dot"></span>
          API Online
        </div>

      </header>


      {/* ================= MAIN CONTENT ================= */}

      <main className="main-content">


        {/* ================================================= */}
        {/* INITIAL INPUT SCREEN */}
        {/* ================================================= */}

        {!result && (
          <>

            <div className="hero">

              <h1>
                Text Summarizer
              </h1>

              <p>
                Turn long text into a clear, concise summary.
              </p>

            </div>


            <div className="input-card">

              <div className="card-header">

                <span>
                  Original Text
                </span>

                <span className="character-count">
                  {text.length} characters
                </span>

              </div>


              <textarea
                value={text}
                onChange={(e) =>
                  setText(e.target.value)
                }
                placeholder="Paste the text you want to summarize..."
              />

            </div>


            <button
              className="summarize-button"
              onClick={handleSummarize}
              disabled={
                loading ||
                !text.trim()
              }
            >

              {loading
                ? "Summarizing..."
                : "✨ Summarize"}

            </button>

          </>
        )}


        {/* ================================================= */}
        {/* SUMMARY TYPE SELECTION */}
        {/* ================================================= */}

        {result && !selectedType && (

          <div className="selection-container">

            <h1>
              Choose your summary
            </h1>

            <p>
              Select how you want your text to be summarized.
            </p>


            <div className="summary-options">


              {/* EXTRACTIVE */}

              <button
                className="summary-option extractive"
                onClick={() =>
                  setSelectedType("extractive")
                }
              >

                <span className="option-icon">
                  🔵
                </span>

                <div>

                  <h2>
                    Extractive
                  </h2>

                  <p>
                    Selects the most important
                    sentences directly from
                    the original text.
                  </p>

                </div>

              </button>


              {/* ABSTRACTIVE */}

              <button
                className="summary-option abstractive"
                onClick={() =>
                  setSelectedType("abstractive")
                }
              >

                <span className="option-icon">
                  🟣
                </span>

                <div>

                  <h2>
                    Abstractive
                  </h2>

                  <p>
                    Uses AI to generate a new
                    concise summary in its own words.
                  </p>

                </div>

              </button>

            </div>


            <button
              className="back-button"
              onClick={handleNewText}
            >
              ← Enter different text
            </button>

          </div>

        )}


        {/* ================================================= */}
        {/* RESULT SCREEN */}
        {/* ================================================= */}

        {result && selectedType && (

          <div className="result-container">


            {/* ================= NAVIGATION ================= */}

            <div className="result-navigation">


              <div className="summary-tabs">

                <button
                  className={`summary-tab extractive ${
                    selectedType === "extractive"
                      ? "active"
                      : ""
                  }`}
                  onClick={() =>
                    setSelectedType("extractive")
                  }
                >
                  🔵 Extractive
                </button>


                <button
                  className={`summary-tab abstractive ${
                    selectedType === "abstractive"
                      ? "active"
                      : ""
                  }`}
                  onClick={() =>
                    setSelectedType("abstractive")
                  }
                >
                  🟣 Abstractive
                </button>

              </div>


              {/* NEW TEXT BUTTON */}

              <button
                className="new-text-button"
                onClick={handleNewText}
              >
                ✨ New Text
              </button>

            </div>


            {/* ================= RESULT HEADING ================= */}

            <div className="result-heading">

              <h1>

                {selectedType === "extractive"
                  ? "Extractive Summarization"
                  : "Abstractive Summarization"}

              </h1>


              <p>

                {selectedType === "extractive"
                  ? "Selects the most important sentences directly from your original text."
                  : "Uses AI to understand the original text and generate a new concise summary in its own words."}

              </p>

            </div>


            {/* ================= ORIGINAL TEXT ================= */}

            <div className="result-card">

              <div className="card-header">

                <span>
                  Original Text
                </span>


                <button
                  className="copy-button"
                  onClick={() =>
                    handleCopy(text)
                  }
                >
                  📋 Copy
                </button>

              </div>


              <div className="result-text">
                {text}
              </div>

            </div>


            {/* ================= SUMMARY ================= */}

            <div
              className={`result-card summary-result ${
                selectedType
              }`}
            >

              <div className="card-header">

                <span>

                  {selectedType === "extractive"
                    ? "Extractive Summary"
                    : "Abstractive Summary"}

                </span>


                <button
                  className="copy-button"
                  onClick={() =>
                    handleCopy(
                      selectedType === "extractive"
                        ? result.extractive_summary
                        : result.abstractive_summary
                    )
                  }
                >
                  📋 Copy
                </button>

              </div>


              <div className="result-text">

                {selectedType === "extractive"
                  ? result.extractive_summary
                  : result.abstractive_summary}

              </div>

            </div>

          </div>

        )}

      </main>


      {/* ================= FOOTER ================= */}

      <footer>

        Powered by{" "}
        <strong>
          PyTextRank
        </strong>

        {" + "}

        <strong>
          DistilBART
        </strong>

      </footer>

    </div>
  );
}

export default App;

