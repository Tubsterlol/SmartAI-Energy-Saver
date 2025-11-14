import React, { useState } from "react";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import UploadSection from "../components/UploadSection";
import ChartsSection from "../components/ChartsSection";
import "../styles/Dashboard.css";

function Dashboard() {
  const [activeSection, setActiveSection] = useState("overview");

  return (
    <div className="dashboard">
      <Header />
      <div className="dashboard-body">
        <Sidebar
          activeSection={activeSection}
          setActiveSection={setActiveSection}
        />

        <main className="dashboard-content">
          {activeSection === "overview" && <h2>Dashboard Overview</h2>}
          {activeSection === "upload" && <UploadSection />}
          {activeSection === "insights" && <h2>Insights</h2>}
          {activeSection === "charts" && <ChartsSection />}
          {activeSection === "forecast" && <h2>Forecast</h2>}
          {activeSection === "tips" && <h2>Green Tips</h2>}
          {activeSection === "about" && <h2>About SmartAI</h2>}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
