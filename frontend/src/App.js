import React, {useEffect} from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useNavigate} from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { logout } from "./services/api";
import Dashboard from "./components/Dashboard";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import RiskMap from "./components/RiskMap";
import HomePage from "./components/HomePage";
import AboutPage from "./components/AboutPage";
import HowItWorks from "./components/HowItWorks";
import ForgotPassword from "./components/ForgotPassword";
import WelcomePage from "./components/WelcomePage";
import MitigationReport from "./components/MitigationReport.jsx";
import AccountSettings from "./components/AccountSettings.js";



import AccountDashboard from "./components/AccountDashboard";

const SessionHandler = () => {
  const navigate = useNavigate();

  useEffect(() => {
    let timeout;

    const resetTimer = () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        logoutUser();
      }, 15 * 60 * 1000); // 15 minutes
    };

    const logoutUser = async () => {
      try {
        await logout();
        localStorage.clear();
        alert("Session expired. Please log in again.");
        navigate("/login");
      } catch (err) {
        console.error("❌ Session timeout logout failed:", err);
        // Still clear session locally even if backend logout fails
        localStorage.clear();
        navigate("/login");
      }
    };

    // Track user activity
    window.onload = resetTimer;
    window.onmousemove = resetTimer;
    window.onmousedown = resetTimer;
    window.ontouchstart = resetTimer;
    window.onclick = resetTimer;
    window.onkeypress = resetTimer;
    window.addEventListener("scroll", resetTimer, true);

    return () => {
      clearTimeout(timeout);
      window.removeEventListener("scroll", resetTimer, true);
    };
  }, [navigate]);

  return null;
};


// Create a custom theme (optional)
const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <SessionHandler /> {/* Automatically logs out inactive users */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/forgot_password" element={<ForgotPassword/>} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/map" element={<RiskMap />} />
          <Route path="/welcome" element={<WelcomePage />} />
          <Route path="/account" element={<AccountDashboard />} />

          <Route path="/mitigation-report" element={<MitigationReport />} />
          <Route path="/account-settings" element={<AccountSettings />} />
          <Route path="/how-it-works" element={<HowItWorks />} /> {/* Added How It Works Page */}
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
