// EditLocation.jsx
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
  Alert,
  Dialog,
  DialogTitle,
  DialogContent
} from "@mui/material";
import EditForm from "./EditForm";

const EditLocation = () => {
  const [locations, setLocations] = useState([]);
  const [error, setError] = useState("");
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [open, setOpen] = useState(false);

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

  useEffect(() => {
    fetchLocations();
  }, []);

  const handleEditClick = (location) => {
    setSelectedLocation(location);
    setOpen(true);
  };

  const handleDialogClose = () => {
    setOpen(false);
    setSelectedLocation(null);
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" sx={{ mb: 3, color: "#1B3A57" }}>
        ✏️ Edit Hotel Locations
      </Typography>

      {error && <Alert severity="error">{error}</Alert>}

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
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
                  <Button variant="outlined" onClick={() => handleEditClick(loc)}>
                    Edit
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleDialogClose} fullWidth maxWidth="sm">

        <DialogContent dividers>
          {selectedLocation && (
            <EditForm
              locationData={selectedLocation}
              onUpdate={fetchLocations}
              onClose={handleDialogClose}
            />
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default EditLocation;
