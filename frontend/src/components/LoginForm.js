import React, { useState } from "react";
import { Box, TextField, Button, Typography, Link, Grid, Container } from "@mui/material";
import Layout from "./Layout";
import { login } from "../services/api";
import { useAuth } from "../context/AuthContext";
import { useNavigate, useLocation } from "react-router-dom";


const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login: authLogin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }

    if (!validateEmail(email)) {
      setError("Invalid email format.");
      return;
    }

    setLoading(true);

    try {
      console.log("🔍 LOGIN DEBUG: Starting login request...");
      console.log("🔍 LOGIN DEBUG: Email:", email);
      console.log("🔍 LOGIN DEBUG: API URL being used:", process.env.NODE_ENV === 'production' ? 'https://bioscope-project-production.up.railway.app' : 'http://localhost:5000');
      
      const response = await login({ email, password });
      
      console.log("🔍 LOGIN DEBUG: Full API response:", response);
      console.log("🔍 LOGIN DEBUG: Response status:", response.status);
      console.log("🔍 LOGIN DEBUG: Response headers:", response.headers);
      console.log("🔍 LOGIN DEBUG: Response data:", response.data);
      
      if (response.data) {
        console.log("🔍 LOGIN DEBUG: Checking response data structure:");
        console.log("- Has user:", !!response.data.user);
        console.log("- Has token:", !!response.data.token);
        console.log("- User data:", response.data.user);
        console.log("- Token data:", response.data.token ? `${response.data.token.substring(0, 20)}...` : "NULL");
        console.log("- Message:", response.data.message);
        console.log("- Error:", response.data.error);
      }

      if (response.data && response.data.user) {
        // SESSION-based login - only need user data
        console.log("✅ LOGIN DEBUG: User present - proceeding with session login");
        authLogin(response.data.user);
        console.log("✅ SESSION Login successful, user:", response.data.user.email);
        
        // Redirect to intended page or account dashboard
        const redirectTo = location.state?.from?.pathname || "/account";
        console.log("✅ Redirecting to:", redirectTo);
        navigate(redirectTo, { replace: true });
      } else if (response.data && response.data.error) {
        console.error("❌ LOGIN DEBUG: Server returned error:", response.data.error);
        setError(response.data.error);
      } else {
        console.error("❌ LOGIN DEBUG: Unexpected response structure:");
        console.error("- Full response:", response);
        console.error("- Response data:", response.data);
        setError("Login failed. Unexpected server response. Check browser console for details.");
      }
    } catch (err) {
      console.error("❌ Login failed:", err);
      
      let errorMessage = "An error occurred during login.";
      
      if (err.code === 'ECONNABORTED' || err.code === 'NETWORK_ERROR') {
        errorMessage = "⚠️ Cannot connect to server. Please check if the backend is running.";
      } else if (err.response?.status === 404) {
        errorMessage = "⚠️ Login endpoint not found. Backend server may not be properly deployed.";
      } else if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.message && err.message.includes('Network Error')) {
        errorMessage = "🌐 Cannot connect to server. Please try again.";
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }

  };

  return (
    <Layout>
      {/* ✅ Full-Width Background, Centered Content */}
      <Box
        sx={{
          width: "100vw",
          minHeight: "60vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          textAlign: "center",
          background: "linear-gradient(135deg, #1B3A57, #4b82c7)",
          color: "white",
          padding: "5% 0",
        }}
      >
        {/* 🔹 Login Box - Styled Like Home Page */}
        <Container
            maxWidth="sm"
          sx={{
            background: "rgba(255, 255, 255, 0.15)",
            textAlign: "center",
            padding: "4%",
            borderRadius: "15px",

            backdropFilter: "blur(12px)",
            boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)",
            margin: "0 auto",
          }}
        >
          <Typography variant="h4" fontWeight="bold" sx={{ fontSize: "clamp(1.8rem, 3vw, 2.5rem)" }}>
            Sign In
          </Typography>

          {/* 🔹 Error Message */}
          {error && (
            <Typography color="error" align="center" sx={{ mt: 2 }}>
              {error}
            </Typography>
          )}

          {/* 🔹 Login Form */}
          <Box component="form" onSubmit={handleSubmit} sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 3 }}>
            <TextField
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              fullWidth
              required
              variant="outlined"
              InputLabelProps={{ style: { color: "#ffffff99" } }}
              InputProps={{
                sx: {
                  background: "rgba(255, 255, 255, 0.2)",
                  borderRadius: "8px",
                  color: "white",
                  "& fieldset": { borderColor: "rgba(255, 255, 255, 0.5)" },
                  "&:hover fieldset": { borderColor: "white" },
                  "&.Mui-focused fieldset": { borderColor: "#4CAF50" },
                },
              }}
            />
            <TextField
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              fullWidth
              required
              variant="outlined"
              InputLabelProps={{ style: { color: "#ffffff99" } }}
              InputProps={{
                sx: {
                  background: "rgba(255, 255, 255, 0.2)",
                  borderRadius: "8px",
                  color: "white",
                  "& fieldset": { borderColor: "rgba(255, 255, 255, 0.5)" },
                  "&:hover fieldset": { borderColor: "white" },
                  "&.Mui-focused fieldset": { borderColor: "#4CAF50" },
                },
              }}
            />

            {/* 🔹 Forgot Password */}
            <Typography align="right" sx={{ fontSize: 14 }}>
              <Link href="/forgot_password" underline="hover" sx={{ color: "white", fontWeight: "bold" }}>
                Forgot Password?
              </Link>
            </Typography>

            {/* 🔹 Login Button */}
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading}
              sx={{
                background: "linear-gradient(90deg, #4CAF50, #388E3C)",
                color: "white",
                borderRadius: "8px",
                padding: "14px 0",
                fontSize: "16px",
                fontWeight: "bold",
                "&:hover": {
                  background: "linear-gradient(90deg, #45a049, #2e7d32)",
                },
              }}
            >
              {loading ? "Logging in..." : "Login"}
            </Button>
          </Box>

          {/* 🔹 Register Link */}
          <Typography align="center" sx={{ mt: 3, fontSize: 14, color: "#ffffff99" }}>
            Don’t have an account?{" "}
            <Link href="/register" underline="hover" sx={{ color: "white", fontWeight: "bold" }}>
              Register
            </Link>
          </Typography>
        </Container>
      </Box>
    </Layout>
  );
};

export default LoginForm;
