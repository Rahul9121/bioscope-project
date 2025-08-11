import React, { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "@mui/material"; // Fix incorrect import
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();
  const [sessionActive, setSessionActive] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await axios.get("http://localhost:5001/session-status");
        setSessionActive(response.data.active);
      } catch (err) {
        setSessionActive(false);
        localStorage.clear();
        alert("Session expired. Please log in again.");
        navigate("/login");
      }
    };

    // Check session status every 5 minutes
    const interval = setInterval(checkSession, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, [navigate]);

  const handleLogout = async () => {
    try {
      await axios.post("http://localhost:5001/logout"); // Logout API
      localStorage.clear(); // Clear user session data
      alert("Logged out successfully.");
      navigate("/login"); // Redirect to login page
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      {sessionActive ? (
        <>
          <h1>Welcome to the Dashboard!</h1>
          <Button
            onClick={handleLogout}
            variant="contained"
            sx={{ backgroundColor: "#d32f2f", "&:hover": { backgroundColor: "#b71c1c" }, marginTop: "20px" }}
          >
            Logout
          </Button>
        </>
      ) : (
        <h1>Session Expired</h1>
      )}
    </div>
  );
};

export default Dashboard;
