import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import RiskMap from "./components/RiskMap";
import MitigationReport from "./components/MitigationReport";
import RegisterForm from "./components/RegisterForm";
import LoginForm from "./components/LoginForm";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/map" element={<RiskMap />} />
        <Route path="/mitigation-report" element={<MitigationReport />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/login" element={<LoginForm />} />
      </Routes>
    </Router>
  );
};

export default App;
