import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import RiskMap from "./components/RiskMap";
import MitigationReport from "./components/MitigationReport";
import RegisterForm from "./components/RegisterForm";
import LoginForm from "./components/LoginForm";
import AccountDashboard from "./components/AccountDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/map" element={<RiskMap />} />
          <Route path="/mitigation-report" element={<MitigationReport />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/account" element={
            <ProtectedRoute>
              <AccountDashboard />
            </ProtectedRoute>
          } />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
