import React from "react";
import "../styles/AboutSection.css"

function AboutSection() {
  return (
    <div className="about-box">
      <h2>About This Project</h2>

      <p>
        This platform helps users upload electricity bill data, analyze patterns,
        generate CO₂ emission trends using linear regression, visualize energy
        insights, and track environmental impact over time. The goal is to make
        energy awareness simple, accessible, and useful for everyday users.
      </p>

      <p>
        Features include CSV upload, forecasting with machine learning,
        CO₂ trend analysis, automated energy-saving tips, and an intuitive
        dashboard built with React and Flask. This provides a smooth experience
        for understanding usage behavior and identifying ways to reduce
        consumption.
      </p>

      <p>
        The project is designed for students, developers, and households who
        want a clean and modern approach to managing electricity data while
        exploring data-driven insights.
      </p>
    </div>
  );
}

export default AboutSection;
