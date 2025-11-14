import React, { useEffect, useState } from "react";
import "../styles/ChartsSection.css";

export default function ChartsSection() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [forecast, setForecast] = useState(null);
  const [plotUrl, setPlotUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetch(`${API_URL}/csv-files`)
      .then((res) => res.json())
      .then((data) => setFiles(data));
  }, []);

  const runModel = async () => {
    if (!selectedFile) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/run-forecast`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: selectedFile }),
      });
      const data = await res.json();
      setForecast(data);
      setPlotUrl(`${API_URL}/forecast_plot.png?${Date.now()}`);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="charts-container">
      <h2>Charts</h2>

      <div className="charts-controls">
        <select
          value={selectedFile}
          onChange={(e) => setSelectedFile(e.target.value)}
        >
          <option value="">Select CSV File</option>
          {files.map((f) => (
            <option key={f} value={f}>
              {f}
            </option>
          ))}
        </select>

        <button onClick={runModel} disabled={loading || !selectedFile}>
          {loading ? "Running..." : "Run Model"}
        </button>
      </div>

      {forecast && (
        <div className="forecast-output">
          <p>Predicted Usage: {forecast.predicted_usage_kWh} kWh</p>
          <p>Predicted Bill: ₹{forecast.predicted_bill_inr}</p>
        </div>
      )}

      {plotUrl && (
        <div className="forecast-output">
          <img src={plotUrl} alt="Forecast Plot" />
        </div>
      )}
    </div>
  );
}
