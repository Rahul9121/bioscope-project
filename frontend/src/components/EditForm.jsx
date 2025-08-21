import React, { useState, useEffect } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Grid,
  Alert
} from "@mui/material";
import axios from "axios";

const EditForm = ({ locationData, onUpdate, onClose }) => {
  const [formData, setFormData] = useState({
    hotel_name: "",
    street_address: "",
    city: "",
    zip_code: ""
  });

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  useEffect(() => {
    if (locationData) {
      setFormData({
        hotel_name: locationData.hotel_name || "",
        street_address: locationData.street_address || "",
        city: locationData.city || "",
        zip_code: locationData.zip_code || ""
      });
    }
  }, [locationData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    setErrorMsg("");
    setSuccessMsg("");
    setLoading(true);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/locations/edit`,
        { ...formData, id: locationData.id },
        { withCredentials: true }
      );

      if (response.status === 200) {
        setSuccessMsg("✅ Location updated successfully.");
        onUpdate();
        onClose();
      }
    } catch (err) {
      console.error("❌ Edit error:", err);
      setErrorMsg("Failed to update location.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        background: "linear-gradient(135deg, #1B3A57, #4b82c7)",
        padding: "2rem",
        borderRadius: "12px",
        boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
        color: "white"
      }}
    >
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        ✏️ Edit Location
      </Typography>

      <Grid container spacing={2} sx={{ mt: 1 }}>
        {[
          { label: "Hotel Name", name: "hotel_name" },
          { label: "Street Address", name: "street_address" },
          { label: "City", name: "city" },
          { label: "Zip Code", name: "zip_code" }
        ].map((field, idx) => (
          <Grid item xs={12} key={idx}>
            <TextField
              fullWidth
              label={field.label}
              name={field.name}
              value={formData[field.name]}
              onChange={handleChange}
              required
              variant="outlined"
              InputLabelProps={{ style: { color: "#ffffffcc" } }}
              InputProps={{
                sx: {
                  background: "rgba(255, 255, 255, 0.2)",
                  borderRadius: "8px",
                  color: "white",
                  "& fieldset": { borderColor: "rgba(255, 255, 255, 0.5)" },
                  "&:hover fieldset": { borderColor: "#ffffff" },
                  "&.Mui-focused fieldset": { borderColor: "#4CAF50" }
                }
              }}
            />
          </Grid>
        ))}
      </Grid>

      {errorMsg && <Alert severity="error" sx={{ mt: 3 }}>{errorMsg}</Alert>}
      {successMsg && <Alert severity="success" sx={{ mt: 3 }}>{successMsg}</Alert>}

      <Box
        sx={{
          display: "flex",
          justifyContent: "flex-end",
          gap: 2,
          mt: 4
        }}
      >
        <Button
          onClick={onClose}
          variant="outlined"
          sx={{
            color: "white",
            borderColor: "white",
            textTransform: "none",
            "&:hover": {
              backgroundColor: "rgba(255,255,255,0.1)"
            }
          }}
        >
          Cancel
        </Button>

        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading}
          sx={{
            background: "linear-gradient(90deg, #4CAF50, #388E3C)",
            color: "white",
            fontWeight: "bold",
            padding: "10px 24px",
            textTransform: "none",
            borderRadius: "8px",
            "&:hover": {
              background: "linear-gradient(90deg, #45a049, #2e7d32)"
            }
          }}
        >
          {loading ? "Saving..." : "Save Changes"}
        </Button>
      </Box>
    </Box>
  );
};

export default EditForm;
