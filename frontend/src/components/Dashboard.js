import React from "react";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout(); // Clear JWT token and user data
    alert("Logged out successfully.");
    navigate("/login"); // Redirect to login page
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      {isAuthenticated() ? (
        <>
          <h1>Welcome to the Dashboard, {user?.email || 'User'}!</h1>
          <Button
            onClick={handleLogout}
            variant="contained"
            sx={{ backgroundColor: "#d32f2f", "&:hover": { backgroundColor: "#b71c1c" }, marginTop: "20px" }}
          >
            Logout
          </Button>
        </>
      ) : (
        <>
          <h1>Authentication Required</h1>
          <p>Please log in to access the dashboard.</p>
        </>
      )}
    </div>
  );
};

export default Dashboard;
