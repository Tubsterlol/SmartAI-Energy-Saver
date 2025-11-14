import React, { useState } from "react";
import "../styles/UploadSection.css";

function UploadSection() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const API_URL = import.meta.env.VITE_API_URL;

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setMessage(data.message || "Upload complete!");
    } catch (error) {
      setMessage("Error uploading file.");
    }
  };

  return (
    <div className="upload-box">
      <h3>Upload Your CSV File</h3>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <p className="note">
        Required columns (in order): Bill_ID, Billing_Month, Billing_Year,
        Units_Consumed_kWh, Total_Amount, Payment_Status
      </p>
      <button onClick={handleUpload}>Upload</button>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default UploadSection;
