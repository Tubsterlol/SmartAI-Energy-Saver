import React from "react";

export default function DashboardOverview() {
  return (
    <div className="overview-container">
      <h2>Dashboard Overview</h2>

      <div className="overview-cards">
        <div className="overview-card">
          <h3>Upload Bills</h3>
          <p>Upload CSV files to start analysis.</p>
        </div>

        <div className="overview-card">
          <h3>Charts & Forecast</h3>
          <p>View usage trends and predictions.</p>
        </div>

        <div className="overview-card">
          <h3>Energy Tips</h3>
          <p>Get AI-generated saving suggestions.</p>
        </div>
      </div>
    </div>
  );
}
