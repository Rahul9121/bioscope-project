import axios from "axios";
import React, { useState } from "react";
import { Box, Button, TextField, Typography, Alert } from "@mui/material";

const AddLocation = () => {
  const [formData, setFormData] = useState({
    hotel_name: "",
    street_address: "",
    city: "",
    zip_code: "",
    email: ""
  });

  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    setError(null);

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/locations/add`, formData, {
        withCredentials: true
      });

      if (response.data.message) {
        setMessage(response.data.message);
        setFormData({
          hotel_name: "",
          street_address: "",
          city: "",
          zip_code: "",
          email: ""
        });
      }
    } catch (err) {
      const msg = err.response?.data?.error || "Something went wrong.";
      setError(msg);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: "bold", color: "#1B3A57" }}>
        Add New Hotel Location
      </Typography>

      <form onSubmit={handleSubmit}>
        {[
          { name: "hotel_name", label: "Hotel Name" },
          { name: "street_address", label: "Street Address" },
          { name: "city", label: "City" },
          { name: "zip_code", label: "Zip Code" },
          { name: "email", label: "Email" }
        ].map((field) => (
          <TextField
            key={field.name}
            name={field.name}
            label={field.label}
            value={formData[field.name]}
            onChange={handleChange}
            fullWidth
            required
            margin="normal"
            variant="outlined"
            InputLabelProps={{ style: { color: "#ffffffcc" } }}
            InputProps={{
              sx: {
                background: "rgba(255, 255, 255, 0.2)",
                borderRadius: "8px",
                color: "white",
                "& fieldset": { borderColor: "rgba(255, 255, 255, 0.5)" },
                "&:hover fieldset": { borderColor: "white" },
                "&.Mui-focused fieldset": { borderColor: "#4CAF50" }
              }
            }}
          />
        ))}

        <Button
          type="submit"
          variant="contained"
          fullWidth
          sx={{
            mt: 2,
            background: "linear-gradient(90deg, #4CAF50, #388E3C)",
            padding: "12px 0",
            fontSize: "16px",
            fontWeight: "bold",
            color: "white",
            borderRadius: "8px",
            "&:hover": {
              background: "linear-gradient(90deg, #45a049, #2e7d32)"
            }
          }}
        >
          Add Location
        </Button>
      </form>

      {message && <Alert severity="success" sx={{ mt: 2 }}>{message}</Alert>}
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
    </Box>
  );
};

export default AddLocation;
