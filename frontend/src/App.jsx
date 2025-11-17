import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import ChartsSection from "./components/ChartsSection";
import TipsSection from "./components/TipsSection"
import CO2Section from "./components/CO2Tracker";
import AboutSection from "./components/AboutSection";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/charts" element={<ChartsSection />} />
        <Route path ="/tips" element={<TipsSection />} />
        <Route path ="/co2-plot" element={<CO2Section/>}/>
        <Route path ="/about" element={<AboutSection/>}/>
      </Routes>
    </Router>
  );
}

export default App;
