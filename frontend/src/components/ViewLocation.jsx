import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button
} from "@mui/material";
import axios from "axios";

const ViewLocation = () => {
  const [locations, setLocations] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await fetch("http://localhost:5001/locations/view", {
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

    fetchLocations();
  }, []);

  const handleReportClick = async (location) => {
    try {
      const { latitude, longitude } = location;

      const response = await axios.post(
        "http://localhost:5001/search",
        { input_text: `${latitude}, ${longitude}` },
        {
          headers: { "Content-Type": "application/json" },
          withCredentials: true,
        }
      );

      if (response.status === 200 && response.data.risks) {
        localStorage.setItem("mitigation_risks", JSON.stringify(response.data.risks));
        window.open("/mitigation-report", "_blank");
      } else {
        alert("Failed to generate report.");
      }
    } catch (error) {
      console.error("Report generation error:", error);
      alert("Error generating report.");
    }
  };

  return (
    <Box>
      <Typography
        variant="h4"
        fontWeight="bold"
        sx={{ mb: 3, color: "#1B3A57" }}
      >
        🗂️ Hotel Locations
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {locations.length === 0 ? (
        <Alert severity="info">No hotel locations available.</Alert>
      ) : (
        <TableContainer component={Paper} sx={{ backgroundColor: "white" }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>Hotel Name</strong></TableCell>
                <TableCell><strong>Address</strong></TableCell>
                <TableCell><strong>City</strong></TableCell>
                <TableCell><strong>ZIP Code</strong></TableCell>
                <TableCell><strong>Latitude</strong></TableCell>
                <TableCell><strong>Longitude</strong></TableCell>
                <TableCell><strong>Report</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {locations.map((loc, index) => (
                <TableRow key={index}>
                  <TableCell>{loc.hotel_name}</TableCell>
                  <TableCell>{loc.street_address}</TableCell>
                  <TableCell>{loc.city}</TableCell>
                  <TableCell>{loc.zip_code}</TableCell>
                  <TableCell>{loc.latitude.toFixed(5)}</TableCell>
                  <TableCell>{loc.longitude.toFixed(5)}</TableCell>
                  <TableCell>
                    <Button
                      variant="contained"
                      color="primary"
                      size="small"
                      onClick={() => handleReportClick(loc)}
                    >
                      View Report
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default ViewLocation;
