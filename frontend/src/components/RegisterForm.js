import React, { useState } from "react";
import { Box, TextField, Button, Typography, Link, Container } from "@mui/material";
import { motion } from "framer-motion";
import Layout from "./Layout";
import axios from "axios";

const RegisterForm = () => {
  const [hotelName, setHotelName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const isPasswordValid = (pwd) => {
    return (
      pwd.length >= 6 &&
      /[A-Za-z]/.test(pwd) &&
      /\d/.test(pwd) &&
      /[!@#$%^&*()_\-+={}\[\]:;"'<>,.?/]/.test(pwd)
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    if (password !== confirmPassword) {
      setMessage("Passwords do not match.");
      setSuccess(false);
      return;
    }

    if (!isPasswordValid(password)) {
      setMessage("Password must be at least 6 characters, contain a letter, number, and special character.");
      setSuccess(false);
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:5001/register",
        { hotel_name: hotelName, email, password },
        { headers: { "Content-Type": "application/json" }, withCredentials: true }
      );

      setSuccess(true);
      setMessage(response.data.message || "Registration successful! You can now log in.");
    } catch (err) {
      setSuccess(false);
      const errorMessage = err.response?.data?.error || "An error occurred during registration.";
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
            borderRadius: "15px",
            backdropFilter: "blur(15px)",
            WebkitBackdropFilter: "blur(15px)",
            boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)",
            padding: "4%",
            textAlign: "center",
          }}
        >
          <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
            <Typography variant="h4" fontWeight="bold" sx={{ fontSize: "clamp(1.8rem, 3vw, 2.5rem)" }}>
              Create Your Account
            </Typography>
          </motion.div>

          {message && (
            <Typography align="center" color={success ? "green" : "error"} sx={{ mt: 2 }}>
              {message}
            </Typography>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 3 }}>
            <motion.div whileFocus={{ scale: 1.05 }} transition={{ duration: 0.3 }}>
              <TextField
                label="Hotel Name"
                type="text"
                value={hotelName}
                onChange={(e) => setHotelName(e.target.value)}
                fullWidth
                required
                variant="outlined"
                InputProps={{
                  sx: textFieldStyle,
                }}
              />
            </motion.div>

            <motion.div whileFocus={{ scale: 1.05 }} transition={{ duration: 0.3 }}>
              <TextField
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                fullWidth
                required
                variant="outlined"
                InputProps={{
                  sx: textFieldStyle,
                }}
              />
            </motion.div>

            <motion.div whileFocus={{ scale: 1.05 }} transition={{ duration: 0.3 }}>
              <TextField
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                fullWidth
                required
                variant="outlined"
                helperText="At least 6 characters, 1 letter, 1 number, 1 special character."
                InputProps={{
                  sx: textFieldStyle,
                }}
              />
            </motion.div>

            <motion.div whileFocus={{ scale: 1.05 }} transition={{ duration: 0.3 }}>
              <TextField
                label="Confirm Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                fullWidth
                required
                variant="outlined"
                InputProps={{
                  sx: textFieldStyle,
                }}
              />
            </motion.div>

            <motion.div whileHover={{ scale: 1.05 }} transition={{ duration: 0.3 }}>
              <Button
                type="submit"
                variant="contained"
                fullWidth
                disabled={loading}
                sx={buttonStyle}
              >
                {loading ? "Registering..." : "Register"}
              </Button>
            </motion.div>
          </Box>

          <Typography align="center" sx={{ mt: 3, fontSize: 14, color: "#ffffff99" }}>
            Already have an account?{" "}
            <Link href="/login" underline="hover" sx={{ color: "white", fontWeight: "bold" }}>
              Login
            </Link>
          </Typography>
        </Container>
      </Box>
    </Layout>
  );
};

export default RegisterForm;

/* ✅ Text Field Styling */
const textFieldStyle = {
  background: "rgba(255, 255, 255, 0.2)",
  borderRadius: "8px",
  color: "white",
  "& fieldset": { borderColor: "rgba(255, 255, 255, 0.5)" },
  "&:hover fieldset": { borderColor: "white" },
  "&.Mui-focused fieldset": { borderColor: "#4CAF50" },
};

/* ✅ Button Styling */
const buttonStyle = {
  background: "linear-gradient(90deg, #4CAF50, #388E3C)",
  color: "white",
  borderRadius: "8px",
  padding: "14px 0",
  fontSize: "16px",
  fontWeight: "bold",
  "&:hover": {
    background: "linear-gradient(90deg, #45a049, #2e7d32)",
  },
};
