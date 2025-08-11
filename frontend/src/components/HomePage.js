import React from "react";
import { Box, Typography, Button, Grid, Container } from "@mui/material";
import Layout from "./Layout";
import { motion } from "framer-motion";

const HomePage = () => {
  return (
    <Layout>
      {/* ✅ Hero Section - Perfectly Centered */}
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
        <Box
          sx={{
            width: "80%",
            maxWidth: "700px",
            textAlign: "center",
            padding: "3%",
            borderRadius: "15px",
            background: "rgba(255, 255, 255, 0.1)",
            backdropFilter: "blur(12px)",
            boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)",
            margin: "0 auto",
          }}
        >
          <Typography variant="h2" fontWeight="bold" sx={{ fontSize: "clamp(2rem, 4vw, 3rem)" }}>
            Welcome to BiodivProScope
          </Typography>
          <Typography variant="h5" sx={{ mt: 2, opacity: 0.9 }}>
            Discover biodiversity insights and protect your environment with data-driven assessments.
          </Typography>
          <Button variant="contained" sx={{ mt: 3, background: "#4CAF50", fontSize: "1.2rem" }}>
            Get Started
          </Button>
        </Box>
      </Box>
    </Layout>
  );
};

export default HomePage;
