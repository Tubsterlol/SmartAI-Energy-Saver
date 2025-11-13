import React, { useState } from "react";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import "../styles/Dashboard.css";

function Dashboard() {
  const [activeSection, setActiveSection] = useState("overview");

  const sections = {
    overview: "Dashboard Overview",
    upload: "Upload Data",
    insights: "Insights",
    charts: "Charts",
    forecast: "Forecast",
    tips: "Green Tips",
    about: "About SmartAI",
  };

  return (
    <div className="dashboard">
      <Header />
      <div className="dashboard-body">
        <Sidebar
          activeSection={activeSection}
          setActiveSection={setActiveSection}
        />
        <main className="dashboard-content">
          <h2>{sections[activeSection]}</h2>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
