import { useState } from "react";
import "./index.css";

function App() {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSummarize = async () => {
    setLoading(true);
    setSummary("");
    setError("");
    try {
      const response = await fetch("http://127.0.0.1:8000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSummary(data.summary || "No summary returned");
    } catch (err) {
      console.error(err);
      setError("Error summarizing text. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="app-container" style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1 style={{ textAlign: "center" }}>Text Summarizer</h1>
      
      <textarea
        placeholder="Paste your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={8}
        style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
      />

      <button
        onClick={handleSummarize}
        disabled={loading || !text.trim()}
        style={{ marginTop: "1rem", padding: "0.5rem 1rem", fontSize: "1rem", cursor: "pointer" }}
      >
        {loading ? "Summarizing..." : "Summarize"}
      </button>

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      {summary && (
        <div className="summary-box" style={{ marginTop: "1rem", padding: "1rem", border: "1px solid #ddd", borderRadius: 8, backgroundColor: "#f9f9f9" }}>
          <h2>Summary:</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;
