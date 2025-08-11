import React, { useState } from "react";
import { Box, TextField, Button, Typography, Link, Container } from "@mui/material";
import Layout from "./Layout";
import axios from "axios";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const validatePassword = (pwd) => {
    return (
      pwd.length >= 6 &&
      /[A-Za-z]/.test(pwd) &&
      /\d/.test(pwd) &&
      /[!@#$%^&*()_\-+={}[\]:;"'<>,.?/]/.test(pwd)
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    if (!email || !newPassword || !confirmPassword) {
      setMessage("All fields are required.");
      setSuccess(false);
      return;
    }

    if (newPassword !== confirmPassword) {
      setMessage("Passwords do not match.");
      setSuccess(false);
      return;
    }

    if (!validatePassword(newPassword)) {
      setMessage(
        "Password must be at least 6 characters long, contain at least one letter, one number, and one special character."
      );
      setSuccess(false);
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5001/forgot_password", {
        email,
        new_password: newPassword,
      });

      setSuccess(true);
      setMessage(response.data.message || "Password reset successful. Redirecting to login...");

      setTimeout(() => {
        window.location.href = "/login";
      }, 2000);
    } catch (err) {
      setSuccess(false);
      const errorMessage = err.response?.data?.error || "An error occurred.";
      setMessage(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
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
        <Container
          maxWidth="sm"
          sx={{
            background: "rgba(255, 255, 255, 0.15)",
            padding: "4%",
            borderRadius: "15px",
            backdropFilter: "blur(12px)",
            boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)",
            margin: "0 auto",
          }}
        >
          <Typography variant="h4" fontWeight="bold" sx={{ fontSize: "clamp(1.8rem, 3vw, 2.5rem)" }}>
            Reset Password
          </Typography>

          {message && (
            <Typography
              align="center"
              sx={{ mt: 2, color: success ? "lightgreen" : "#ff9494", fontWeight: "bold" }}
            >
              {message}
            </Typography>
          )}

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
              label="New Password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              fullWidth
              required
              variant="outlined"
              helperText="At least 6 characters, 1 letter, 1 number, 1 special character."
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
              label="Confirm Password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
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
              {loading ? "Resetting..." : "Reset Password"}
            </Button>
          </Box>

          <Typography align="center" sx={{ mt: 3, fontSize: 14, color: "#ffffff99" }}>
            Remembered your password?{" "}
            <Link href="/login" underline="hover" sx={{ color: "white", fontWeight: "bold" }}>
              Login
            </Link>
          </Typography>
        </Container>
      </Box>
    </Layout>
  );
};

export default ForgotPassword;
