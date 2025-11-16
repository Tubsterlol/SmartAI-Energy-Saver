import React, { useState } from "react";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import UploadSection from "../components/UploadSection";
import ChartsSection from "../components/ChartsSection";
import TipsSection from "../components/TipsSection";
import DashboardOverview from "../components/DashboardOverview";
import CO2Section from "../components/CO2Tracker";
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
          {activeSection === "overview" && <DashboardOverview />}
          {activeSection === "upload" && <UploadSection />}
          {activeSection === "co2-tracker" && <CO2Section />}
          {activeSection === "prediction" && <ChartsSection />}
          {activeSection === "tips" && <TipsSection />}
          {activeSection === "about" && <h2>About SmartAI</h2>}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
