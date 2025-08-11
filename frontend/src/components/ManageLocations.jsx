// ManageLocations.jsx
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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert
} from "@mui/material";
import axios from "axios";
import EditForm from "./EditForm";

const ManageLocations = () => {
  const [locations, setLocations] = useState([]);
  const [error, setError] = useState("");
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

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

  const handleDelete = async () => {
    try {
      const response = await fetch("http://localhost:5001/locations/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(selectedLocation)
      });

      const result = await response.json();
      if (response.ok) {
        fetchLocations();
        setShowDeleteConfirm(false);
        setSelectedLocation(null);
      } else {
        alert(result.error || "Failed to delete location.");
      }
    } catch (err) {
      alert("Server error during deletion.");
    }
  };

  return (
    <Box>
      <Typography
        variant="h4"
        fontWeight="bold"
        sx={{ mb: 3, color: "#1B3A57" }}
      >
        🛠️ Manage Hotel Locations
      </Typography>

      {error && <Alert severity="error">{error}</Alert>}

      <TableContainer component={Paper} sx={{ borderRadius: 3 }}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead sx={{ backgroundColor: "#1B3A57" }}>
            <TableRow>
              <TableCell sx={{ color: "white" }}>Hotel Name</TableCell>
              <TableCell sx={{ color: "white" }}>Street Address</TableCell>
              <TableCell sx={{ color: "white" }}>City</TableCell>
              <TableCell sx={{ color: "white" }}>Zip Code</TableCell>
              <TableCell sx={{ color: "white" }}>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {locations.map((loc, index) => (
              <TableRow key={index}>
                <TableCell>{loc.hotel_name}</TableCell>
                <TableCell>{loc.street_address}</TableCell>
                <TableCell>{loc.city}</TableCell>
                <TableCell>{loc.zip_code}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    sx={{ mr: 1 }}
                    onClick={() => setSelectedLocation(loc)}
                  >
                    Edit
                  </Button>
                  <Button
                    variant="contained"
                    color="error"
                    onClick={() => {
                      setSelectedLocation(loc);
                      setShowDeleteConfirm(true);
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

      {selectedLocation && (
        <EditForm
          open={!!selectedLocation && !showDeleteConfirm}
          locationData={selectedLocation}
          onClose={() => setSelectedLocation(null)}
          onUpdate={fetchLocations}
        />
      )}

      {/* Delete confirmation dialog */}
      <Dialog open={showDeleteConfirm} onClose={() => setShowDeleteConfirm(false)}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          Are you sure you want to delete the location "{selectedLocation?.hotel_name}"?
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDeleteConfirm(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={handleDelete} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ManageLocations;
