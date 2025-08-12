import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import RiskMap from "./components/RiskMap";
import MitigationReport from "./components/MitigationReport";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/map" element={<RiskMap />} />
        <Route path="/mitigation-report" element={<MitigationReport />} />
      </Routes>
    </Router>
  );
};

export default App;
