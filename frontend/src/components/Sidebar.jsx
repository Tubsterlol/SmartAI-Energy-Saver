import React from "react";
import "../styles/Sidebar.css";

function Sidebar({ activeSection, setActiveSection }) {
  const sections = ["overview", "upload", "insights", "charts", "forecast", "tips", "about"];

  return (
    <aside className="sidebar">
      <h2 className="sidebar-title">Menu</h2>
      <ul>
        {sections.map((s) => (
          <li
            key={s}
            className={activeSection === s ? "active" : ""}
            onClick={() => setActiveSection(s)}
          >
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default Sidebar;
