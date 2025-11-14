import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import ChartsSection from "./components/ChartsSection";
import TipsSection from "./components/TipsSection"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/charts" element={<ChartsSection />} />
        <Route path ="/tips" element={<TipsSection />} />
      </Routes>
    </Router>
  );
}

export default App;
