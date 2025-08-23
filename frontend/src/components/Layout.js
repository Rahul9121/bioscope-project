import React, { useState, useEffect } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Container,
  Menu,
  MenuItem
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { logout as apiLogout } from "../services/api";

const Layout = ({ children }) => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const { user, logout: authLogout, isAuthenticated, loading } = useAuth();
  
  // Debug authentication state
  console.log("🏢 Layout Debug:");
  console.log("- User from AuthContext:", user);
  console.log("- Loading state:", loading);
  console.log("- isAuthenticated():", isAuthenticated());
  console.log("- localStorage user:", localStorage.getItem("user"));
  console.log("- Should show authenticated nav:", isAuthenticated());

  const handleLogout = async () => {
    try {
      // Call backend logout API
      await apiLogout();
      console.log("✅ Backend logout successful");
    } catch (error) {
      console.error("⚠️ Logout API failed:", error);
      // Continue with local logout even if API fails
    } finally {
      // Always clear local auth state
      authLogout();
      navigate("/");
      console.log("✅ User logged out and redirected");
    }
  };

  const handleNavigation = (path) => {
    navigate(path);
  };

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleAccountClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleAccountClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
        width: "100vw",
        maxWidth: "100vw",
        overflowX: "hidden",
        margin: "0 auto",
        alignItems: "center",
        background: "linear-gradient(135deg, #F3F3F3, #E0E0E0)",
        color: "#222"
      }}
    >
      <AppBar
        position="sticky"
        sx={{
          background: "linear-gradient(135deg, #4CAF50, #388E3C)",
          backdropFilter: "blur(12px)",
          boxShadow: "0px 4px 12px rgba(76, 175, 80, 0.4)",
          padding: "24px 0",
          width: "100%",
          borderBottom: "2px solid rgba(0, 0, 0, 0.1)"
        }}
      >
        <Toolbar sx={{ justifyContent: "space-between", minHeight: 100, padding: "0 6%" }}>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              cursor: "pointer"
            }}
            onClick={() => navigate("/")}
          >
            <Typography variant="h2" sx={{ fontWeight: "bold", fontSize: "2.8rem", color: "white", transition: "0.3s", "&:hover": { opacity: 0.8 } }}>
              BiodivProScope
            </Typography>
            <Typography variant="body1" sx={{ color: "rgba(255,255,255,0.9)", fontSize: "1.1rem", marginTop: "0px" }}>
              Advanced Biodiversity Risk Insights
            </Typography>
          </Box>

          <Box sx={{ display: { xs: "none", md: "flex" }, gap: 4 }}>
            <Button onClick={() => handleNavigation("/")} sx={navButtonStyle}>Home</Button>
            <Button onClick={() => handleNavigation("/about")} sx={navButtonStyle}>About</Button>
            <Button onClick={() => handleNavigation("/how-it-works")} sx={navButtonStyle}>How It Works</Button>
            <Button onClick={() => handleNavigation("/map")} sx={navButtonStyle}>Risk Assessment</Button>
          </Box>

          <Box sx={{ display: "flex", alignItems: "center", gap: 3 }}>
            {isAuthenticated() ? (
              <>
                <Button
                  onClick={handleAccountClick}
                  sx={{ ...navButtonStyle, position: "relative" }}
                >
                  Account
                </Button>
                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleAccountClose}
                  PaperProps={{
                    sx: {
                      mt: 1,
                      minWidth: 200,
                      borderRadius: 2,
                      background: "#f8f8f8"
                    }
                  }}
                >
                  <MenuItem onClick={() => { handleAccountClose(); navigate("/account-settings"); }}>Account Settings</MenuItem>
                  <MenuItem onClick={() => { handleAccountClose(); navigate("/account"); }}>Manage Locations</MenuItem>
                </Menu>
                <Button
                  variant="outlined"
                  onClick={handleLogout}
                  sx={{
                    ...navButtonStyle,
                    border: "2px solid white",
                    "&:hover": {
                      background: "#66BB6A",
                      border: "2px solid #fff"
                    }
                  }}
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button onClick={() => handleNavigation("/login")} sx={navButtonStyle}>Login</Button>
                <Button
                  variant="outlined"
                  onClick={() => handleNavigation("/register")}
                  sx={{
                    ...navButtonStyle,
                    border: "2px solid white",
                    "&:hover": {
                      background: "#66BB6A",
                      border: "2px solid #fff"
                    }
                  }}
                >
                  Register
                </Button>
              </>
            )}
          </Box>

          <IconButton color="inherit" onClick={toggleDrawer} sx={{ display: { xs: "block", md: "none" } }}>
            <MenuIcon sx={{ fontSize: "2.5rem", color: "white" }} />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Drawer anchor="right" open={drawerOpen} onClose={toggleDrawer}>
        <List sx={{ width: 300 }}>
          <ListItem button onClick={toggleDrawer} component="a" href="/">
            <ListItemText primary="Home" />
          </ListItem>
          <ListItem button onClick={toggleDrawer} component="a" href="/about">
            <ListItemText primary="About" />
          </ListItem>
          <ListItem button onClick={toggleDrawer} component="a" href="/how-it-works">
            <ListItemText primary="How It Works" />
          </ListItem>
          <ListItem button onClick={toggleDrawer} component="a" href="/map">
            <ListItemText primary="Risk Assessment" />
          </ListItem>
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, display: "flex", flexDirection: "column", width: "100%", padding: "0" }}>
        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", width: "100%" }}>
          {children}
        </Box>
      </Box>

      <Box sx={{ py: 4, background: "#2E2E2E", color: "white", textAlign: "center", width: "100%" }}>
        <Container>
          <Typography variant="body1" sx={{ fontSize: "1.2rem" }}>
            &copy; {new Date().getFullYear()} BiodivProScope. All rights reserved.
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.7 }}>
            Built for biodiversity risk assessment and regulatory compliance.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;

const navButtonStyle = {
  fontSize: "1.4rem",
  padding: "14px 28px",
  color: "white",
  fontWeight: "bold",
  borderRadius: "8px",
  transition: "0.3s ease-in-out",
  background: "transparent",
  border: "2px solid rgba(255, 255, 255, 0.2)",
  "&:hover": {
    background: "rgba(255, 255, 255, 0.1)",
    border: "2px solid rgba(255, 255, 255, 0.5)",
    transform: "scale(1.08)",
    boxShadow: "0px 4px 12px rgba(76, 175, 80, 0.3)"
  }
};
