import React, { useState, useEffect } from "react";
import "../styles/CO2Tracker.css"

function CO2Section() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [plotUrl, setPlotUrl] = useState("");

  useEffect(() => {
    fetch("http://localhost:5000/csv-files")
      .then(res => res.json())
      .then(data => setFiles(data));
  }, []);

  const generatePlot = async () => {
    const res = await fetch("http://localhost:5000/co2-plot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: selectedFile }),
    });

    const data = await res.json();

    if (data.status === "success") {
      setPlotUrl("http://localhost:5000/co2_plot.png?cache=" + Date.now());
    }
  };

  return (
    <div className="upload-box">
      <h3>CO₂ Linear Regression Trend</h3>

      <select value={selectedFile} onChange={(e) => setSelectedFile(e.target.value)}>
        <option>Select a CSV</option>
        {files.map((f) => (
          <option key={f} value={f}>{f}</option>
        ))}
      </select>

      <button onClick={generatePlot}>Generate CO₂ Trend</button>

      {plotUrl && (
        <div style={{ marginTop: "20px", textAlign: "center" }}>
          <img src={plotUrl} alt="CO2 Plot" style={{ width: "80%", borderRadius: "10px" }} />
        </div>
      )}
    </div>
  );
}

export default CO2Section;
