import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableContainer,
  Paper,
  Button,
  Alert
} from "@mui/material";

const DeleteLocation = () => {
  const [locations, setLocations] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchLocations = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/locations/view`, {
        credentials: "include"
      });
      const data = await response.json();
      if (response.ok) {
        setLocations(data.locations);
      } else {
        setError(data.error || "Unable to fetch locations.");
      }
    } catch (err) {
      setError("Server error. Please try again later.");
    }
  };

  useEffect(() => {
    fetchLocations();
  }, []);

  const handleDelete = async (loc) => {
    setError("");
    setSuccess("");

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/locations/delete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          hotel_name: loc.hotel_name,
          street_address: loc.street_address,
          city: loc.city,
          zip_code: loc.zip_code
        })
      });

      const data = await response.json();
      if (response.ok) {
        setSuccess(data.message || "Location successfully deleted.");
        fetchLocations(); // refresh table
      } else {
        setError(data.error || "Could not delete location.");
      }
    } catch (err) {
      setError("Server error. Please try again later.");
    }
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" sx={{ mb: 3, color: "#1B3A57" }}>
        ❌ Delete Hotel Locations
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="delete location table">
          <TableHead sx={{ backgroundColor: "#1B3A57" }}>
            <TableRow>
              <TableCell sx={{ color: "white" }}>Hotel Name</TableCell>
              <TableCell sx={{ color: "white" }}>Street Address</TableCell>
              <TableCell sx={{ color: "white" }}>City</TableCell>
              <TableCell sx={{ color: "white" }}>Zip Code</TableCell>
              <TableCell sx={{ color: "white" }}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {locations.map((loc, idx) => (
              <TableRow key={idx}>
                <TableCell>{loc.hotel_name}</TableCell>
                <TableCell>{loc.street_address}</TableCell>
                <TableCell>{loc.city}</TableCell>
                <TableCell>{loc.zip_code}</TableCell>
                <TableCell>
                  <Button
                    variant="contained"
                    color="error"
                    onClick={() => handleDelete(loc)}
                    sx={{
                      fontWeight: "bold",
                      borderRadius: "8px",
                      textTransform: "none",
                      background: "linear-gradient(90deg, #e53935, #b71c1c)",
                      "&:hover": {
                        background: "linear-gradient(90deg, #d32f2f, #880e4f)"
                      }
                    }}
                  >
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default DeleteLocation;
