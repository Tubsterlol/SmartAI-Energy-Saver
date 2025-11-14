import React, { useEffect, useState } from "react";
import "../styles/TipsSection.css";

export default function TipsSection() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [tips, setTips] = useState(null);
  const [treeImage, setTreeImage] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL;

  const fetchFiles = () => {
    fetch(`${API_URL}/csv-files`)
      .then((res) => res.json())
      .then((data) => setFiles(data));
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const uploadFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    setUploading(false);
    fetchFiles();
  };

  const runTips = async () => {
    if (!selectedFile) return;
    setLoading(true);

    const res = await fetch(`${API_URL}/run-tips`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: selectedFile }),
    });

    const data = await res.json();

    setTips(data);
    setTreeImage(data.tree_image || "");

    setLoading(false);
  };

  return (
    <div className="tips-container">
      <h2>Energy Tips</h2>

      <div className="tips-upload-box">
        <input type="file" accept=".csv" onChange={uploadFile} />
        {uploading && <p>Uploading...</p>}
      </div>

      <div className="tips-controls">
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

        <button onClick={runTips} disabled={loading || !selectedFile}>
          {loading ? "Generating..." : "Generate Tips"}
        </button>
      </div>

      {tips && (
        <div className="tips-output">
          <h3>Category: {tips.category}</h3>
          {tips.tips.map((t, i) => (
            <p key={i}>{t}</p>
          ))}
        </div>
      )}

      {treeImage && (
        <div className="tips-output">
          <h3>Decision Tree</h3>
          <img
            src={`data:image/png;base64,${treeImage}`}
            alt="Decision Tree"
            className="tree-image"
          />
        </div>
      )}
    </div>
  );
}
