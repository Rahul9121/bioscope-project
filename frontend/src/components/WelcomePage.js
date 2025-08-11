import React from "react";
import { Box, Typography, Button, Card, CardContent, Stack, Divider } from "@mui/material";
import Layout from "./Layout";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const WelcomePage = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axios.post("http://localhost:5001/logout", {}, { withCredentials: true });
      localStorage.removeItem("user");
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <Layout>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
          width: "100%",
          background: "linear-gradient(-45deg, #4caf50, #81c784, #66bb6a, #388e3c)",
          backgroundSize: "400% 400%",
          animation: "gradientShift 12s ease infinite",
          padding: 4,
          "@keyframes gradientShift": {
            "0%": { backgroundPosition: "0% 50%" },
            "50%": { backgroundPosition: "100% 50%" },
            "100%": { backgroundPosition: "0% 50%" },
          },
        }}
      >
        <Card
          sx={{
            width: "100%",
            maxWidth: 600,
            boxShadow: 10,
            borderRadius: 3,
            backgroundColor: "rgba(255,255,255,0.95)",
            px: 3,
            py: 4,
          }}
        >
          <CardContent>
            <Typography variant="h4" align="center" sx={{ fontWeight: "bold", color: "#2E7D32", mb: 2 }}>
              Welcome to BiodivProScope! 🌿
            </Typography>

            <Typography align="center" sx={{ mb: 2 }}>
              You've successfully logged in. Let’s explore how your hotel can become a biodiversity champion.
            </Typography>

            <Divider sx={{ my: 3 }} />

            <Stack spacing={2}>
              <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                🧭 What you can do:
              </Typography>

              <Typography>
                ✅ <strong>Run a Risk Assessment:</strong> Check your hotel's environmental footprint.
              </Typography>
              <Typography>
                ✅ <strong>Explore Biodiversity Maps:</strong> Visualize local species risks and habitats.
              </Typography>
              <Typography>
                ✅ <strong>Download Reports:</strong> Generate compliance-ready mitigation plans.
              </Typography>
              <Typography>
                ✅ <strong>Manage Locations:</strong> Add, edit, or remove hotel properties.
              </Typography>
            </Stack>

            <Divider sx={{ my: 3 }} />

            <Stack direction="row" spacing={2} justifyContent="center" mt={2}>
              <Button
                variant="contained"
                onClick={() => navigate("/map")}
                sx={{
                  backgroundColor: "#2E7D32",
                  "&:hover": { backgroundColor: "#1b5e20" },
                  paddingX: 4,
                }}
              >
                Go to Risk Map
              </Button>
              <Button
                variant="outlined"
                onClick={handleLogout}
                sx={{
                  color: "#2E7D32",
                  borderColor: "#2E7D32",
                  "&:hover": { backgroundColor: "#e8f5e9", borderColor: "#1b5e20" },
                }}
              >
                Logout
              </Button>
            </Stack>
          </CardContent>
        </Card>
      </Box>
    </Layout>
  );
};

export default WelcomePage;
