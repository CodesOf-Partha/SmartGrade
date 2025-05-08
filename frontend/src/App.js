import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('http://localhost:8000/upload-worksheet/', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>SmartGrade: Worksheet Grader</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit" disabled={loading}>{loading ? 'Grading...' : 'Upload & Grade'}</button>
      </form>
      {result && (
        <div className="results">
          <h2>Extracted Text</h2>
          <pre>{result.extracted_text}</pre>
          <h2>Grading Results</h2>
          <ul>
            {result.grading.map((g, idx) => (
              <li key={idx} style={{color: g.correct ? 'green' : 'red'}}>
                <b>Question {g.question}:</b> {g.feedback} (Score: {g.score})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
