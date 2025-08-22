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
import { viewLocations, searchRisks } from "../services/api";

const ViewLocation = () => {
  const [locations, setLocations] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchLocations = async () => {
      try {
        console.log("🗺️ Fetching user locations...");
        const response = await viewLocations();
        
        if (response.data.locations) {
          setLocations(response.data.locations);
          console.log(`✅ Loaded ${response.data.locations.length} locations`);
        } else {
          setError("No locations found.");
        }
      } catch (err) {
        console.error("❌ Error fetching locations:", err);
        
        if (err.response?.status === 401) {
          setError("🔒 Please login first. Your session may have expired.");
          setTimeout(() => {
            window.location.href = "/login";
          }, 3000);
        } else if (err.response?.data?.error) {
          setError(err.response.data.error);
        } else {
          setError("🌐 Server error. Please try again later.");
        }
      }
    };

    fetchLocations();
  }, []);

  const handleReportClick = async (location) => {
    try {
      const { latitude, longitude } = location;
      console.log(`🗺️ Generating report for: ${location.hotel_name}`);

      const response = await searchRisks({ input_text: `${latitude}, ${longitude}` });

      if (response.data && response.data.risks) {
        localStorage.setItem("mitigation_risks", JSON.stringify(response.data.risks));
        console.log("✅ Report data saved, opening report window");
        window.open("/mitigation-report", "_blank");
      } else {
        alert("⚠️ No biodiversity risks found for this location.");
      }
    } catch (error) {
      console.error("❌ Report generation error:", error);
      
      if (error.response?.status === 401) {
        alert("🔒 Please login first to generate reports.");
        setTimeout(() => {
          window.location.href = "/login";
        }, 2000);
      } else {
        alert("❌ Error generating report. Please try again.");
      }
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
