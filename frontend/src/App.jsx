import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import ChartsSection from "./components/ChartsSection";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/charts" element={<ChartsSection />} />
      </Routes>
    </Router>
  );
}

export default App;
