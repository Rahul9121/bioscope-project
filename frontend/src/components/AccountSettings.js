import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Grid,
  Alert,
  Paper,
  Divider,
} from "@mui/material";
import Layout from "./Layout";
import axios from "axios";

const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>/?]).{6,}$/;

const AccountSettings = () => {
  const [profile, setProfile] = useState({ hotel_name: "", email: "" });
  const [passwords, setPasswords] = useState({ current: "", new: "", confirm: "" });
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const parsed = JSON.parse(storedUser);
      setProfile({ hotel_name: parsed.hotel_name || "", email: parsed.email || "" });
    }
  }, []);

  const handleProfileChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handlePasswordChange = (e) => {
    setPasswords({ ...passwords, [e.target.name]: e.target.value });
  };

  const handleProfileSave = async () => {
    try {
      await axios.put(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/account/update-profile`, profile, {
          withCredentials: true,
        });

      setSuccessMsg("Profile updated successfully.");
      setErrorMsg("");
    } catch (error) {
      console.error(error);
      setErrorMsg("Failed to update profile.");
      setSuccessMsg("");
    }
  };

  const handlePasswordSave = async () => {
    const { current, new: newPassword, confirm } = passwords;
    if (newPassword !== confirm) {
      return setErrorMsg("New password and confirmation do not match.");
    }
    if (!passwordRegex.test(newPassword)) {
      return setErrorMsg(
        "Password must be at least 6 characters long and include at least 1 alphabetical character, 1 numerical digit, and 1 special character."
      );
    }

    try {
      await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/account/change-password`, {
        currentPassword: current,
        newPassword: newPassword,
      }, {withCredentials: true});
      setSuccessMsg("Password changed successfully.");
      setErrorMsg("");
    } catch (error) {
      console.error(error);
      setErrorMsg("Failed to change password.");
      setSuccessMsg("");
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
        <Paper
          elevation={6}
          sx={{
            width: "90%",
            maxWidth: 1000,
            p: 5,
            borderRadius: "20px",
            background: "rgba(255,255,255,0.1)",
            backdropFilter: "blur(10px)",
            boxShadow: "0 8px 24px rgba(0,0,0,0.4)",
            color: "white",
          }}
        >
          <Typography variant="h3" fontWeight="bold" gutterBottom>
            ⚙️ Account Settings
          </Typography>

          <Divider sx={{ my: 3, borderColor: "rgba(255,255,255,0.3)" }} />

          <Typography variant="h5" gutterBottom>
            🔐 Update Profile Information
          </Typography>

          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Hotel Name"
                name="hotel_name"
                value={profile.hotel_name}
                onChange={handleProfileChange}
                variant="outlined"
                InputLabelProps={{ shrink: true }}
                sx={{
                  background: "rgba(255, 255, 255, 0.2)",
                  borderRadius: 2,
                  input: { color: "white" },
                  label: { color: "#ffffffcc" },
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Email"
                name="email"
                value={profile.email}
                onChange={handleProfileChange}
                variant="outlined"
                InputLabelProps={{ shrink: true }}
                sx={{
                  background: "rgba(255, 255, 255, 0.2)",
                  borderRadius: 2,
                  input: { color: "white" },
                  label: { color: "#ffffffcc" },
                }}
              />
            </Grid>
          </Grid>

          <Button
            variant="contained"
            sx={{ mt: 3, background: "#4CAF50", fontWeight: "bold" }}
            onClick={handleProfileSave}
          >
            Save Profile
          </Button>

          <Divider sx={{ my: 4, borderColor: "rgba(255,255,255,0.3)" }} />

          <Typography variant="h5" gutterBottom>
            🔒 Change Password
          </Typography>

          <Grid container spacing={3} sx={{ mt: 1 }}>
            {[
              { label: "Current Password", name: "current" },
              { label: "New Password", name: "new" },
              { label: "Confirm New Password", name: "confirm" },
            ].map((field, idx) => (
              <Grid item xs={12} sm={4} key={idx}>
                <TextField
                  fullWidth
                  type="password"
                  label={field.label}
                  name={field.name}
                  value={passwords[field.name]}
                  onChange={handlePasswordChange}
                  variant="outlined"
                  sx={{
                    background: "rgba(255, 255, 255, 0.2)",
                    borderRadius: 2,
                    input: { color: "white" },
                    label: { color: "#ffffffcc" },
                  }}
                />
              </Grid>
            ))}
          </Grid>

          <Button
            variant="contained"
            sx={{ mt: 3, background: "#4CAF50", fontWeight: "bold" }}
            onClick={handlePasswordSave}
          >
            Save Password
          </Button>

          {errorMsg && <Alert severity="error" sx={{ mt: 3 }}>{errorMsg}</Alert>}
          {successMsg && <Alert severity="success" sx={{ mt: 3 }}>{successMsg}</Alert>}
        </Paper>
      </Box>
    </Layout>
  );
};

export default AccountSettings;