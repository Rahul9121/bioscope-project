import React, { useState } from "react";
import {
  Box,
  Typography,
  Button,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemButton,
  Divider
} from "@mui/material";
import Layout from "./Layout";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import AddLocation from "./AddLocation";
import DeleteLocation from "./DeleteLocation";
import ViewLocation from "./ViewLocation";
import EditLocation from "./EditLocation";

const AccountDashboard = () => {
  const [activeModule, setActiveModule] = useState(null);
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const renderModule = () => {
    switch (activeModule) {
      case "add":
        return <AddLocation />;
      case "delete":
        return <DeleteLocation />;
      case "view":
        return <ViewLocation onEditClick={() => setActiveModule("edit")} />;
      case "edit":
        return (
          <EditLocation
            location={{
              hotel_name: "Marvin Hotels",
              street_address: "115 Normal Avenue",
              city: "Montclair",
              zip_code: "07043"
            }}
            onSuccess={() => setActiveModule("view")}
          />
        );
      default:
        return (
          <Box>
            <Typography variant="h5" sx={{ mb: 2 }}>
              🛠️ Select a tool from the sidebar to begin managing your hotel locations.
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9 }}>
              You can add a new hotel, view your registered locations, make updates, or remove old entries using the available options.
            </Typography>
          </Box>
        );
    }
  };

  return (
    <Layout>
      <Box
        sx={{
          width: "100vw",
          minHeight: "70vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "linear-gradient(135deg, #1B3A57, #4b82c7)",
          color: "white",
          padding: "5% 0",
          overflowX: "hidden",
          fontFamily: "'Roboto', sans-serif"
        }}
      >
        <Grid container spacing={4} sx={{ width: "95%", maxWidth: "1400px" }}>
          {/* Sidebar */}
          <Grid item xs={12} sm={4} md={3}>
            <Paper
              elevation={6}
              sx={{
                background: "linear-gradient(145deg, #2E4C6D, #3E6DA3)",
                borderRadius: "20px",
                padding: 5,
                color: "white",
                boxShadow: "0 8px 24px rgba(0,0,0,0.4)"
              }}
            >
              <Typography
                variant="h4"
                fontWeight="bold"
                sx={{
                  mb: 4,
                  fontSize: "clamp(2rem, 3vw, 2.6rem)",
                  textAlign: "left"
                }}
              >
                🧭 Location Panel
              </Typography>
              <Divider sx={{ borderColor: "rgba(255,255,255,0.4)", mb: 3 }} />
              <List>
                {[
                  { key: "add", label: "➕ Add Location" },
                  { key: "view", label: "📋 View Locations" },
                  { key: "edit", label: "✏️ Edit Location" },
                  { key: "delete", label: "🗑️ Delete Location" }
                ].map((item) => (
                  <ListItem disablePadding sx={{ mb: 2 }} key={item.key}>
                    <ListItemButton
                      onClick={() => setActiveModule(item.key)}
                      sx={{
                        fontSize: "1.1rem",
                        fontWeight: 500,
                        borderRadius: 2,
                        py: 1.5,
                        px: 3,
                        background: "rgba(255,255,255,0.08)",
                        color: "#fff",
                        '&:hover': {
                          background: "rgba(255,255,255,0.25)",
                          transform: "scale(1.04)",
                          boxShadow: "0px 0px 10px rgba(255,255,255,0.3)"
                        }
                      }}
                    >
                      {item.label}
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>

          {/* Main Content */}
          <Grid item xs={12} sm={8} md={9}>
            <Box
              sx={{
                background: "rgba(255, 255, 255, 0.15)",
                borderRadius: "16px",
                backdropFilter: "blur(10px)",
                boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.3)",
                padding: "3%",
                color: "white"
              }}
            >
              {user ? (
                <>
                  <Typography variant="h3" fontWeight="bold" sx={{ mb: 2, fontSize: "clamp(2.2rem, 4vw, 2.8rem)" }}>
                    Welcome, {user.hotel_name || "User"}!
                  </Typography>
                  <Typography variant="h6" sx={{ mb: 3, opacity: 0.9 }}>
                    Use the panel to manage your hotel’s biodiversity monitoring locations.
                  </Typography>

                  {renderModule()}

                  <Button
                    variant="outlined"
                    sx={{
                      mt: 4,
                      borderColor: "#4CAF50",
                      color: "#4CAF50",
                      fontWeight: "bold",
                      '&:hover': {
                        backgroundColor: "#4CAF50",
                        color: "#fff"
                      }
                    }}
                    onClick={() => setActiveModule(null)}
                  >
                    Return to Dashboard
                  </Button>
                </>
              ) : (
                <Typography variant="h5" color="error">
                  ⚠️ Unable to retrieve user information. Please log in again.
                </Typography>
              )}
            </Box>
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
};

export default AccountDashboard;
