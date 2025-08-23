import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { useAuth } from '../context/AuthContext';

const AuthDebug = () => {
  const { user, loading, isAuthenticated } = useAuth();

  console.log("🚨 AUTH DEBUG COMPONENT:");
  console.log("- user:", user);
  console.log("- loading:", loading);
  console.log("- isAuthenticated():", isAuthenticated());

  const localStorageUser = localStorage.getItem("user");
  let parsedLocalStorageUser = null;
  try {
    if (localStorageUser && localStorageUser !== "null") {
      parsedLocalStorageUser = JSON.parse(localStorageUser);
    }
  } catch (e) {
    console.error("Error parsing localStorage user:", e);
  }

  return (
    <Paper sx={{ p: 3, m: 2, bgcolor: '#f5f5f5' }}>
      <Typography variant="h6" sx={{ mb: 2, color: 'red' }}>
        🚨 AUTH DEBUG INFO
      </Typography>
      
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>AuthContext user:</strong> {user ? JSON.stringify(user, null, 2) : "NULL"}
      </Typography>
      
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Loading state:</strong> {loading ? "TRUE" : "FALSE"}
      </Typography>
      
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>isAuthenticated():</strong> {isAuthenticated() ? "TRUE" : "FALSE"}
      </Typography>
      
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>localStorage user:</strong> {parsedLocalStorageUser ? JSON.stringify(parsedLocalStorageUser, null, 2) : "NULL"}
      </Typography>
      
      <Typography variant="body2" sx={{ mb: 1 }}>
        <strong>Raw localStorage:</strong> {localStorageUser || "NULL"}
      </Typography>
      
      <Typography variant="body2" sx={{ mb: 1, color: user ? 'green' : 'red' }}>
        <strong>Should show dashboard content:</strong> {user ? "YES ✅" : "NO ❌"}
      </Typography>
    </Paper>
  );
};

export default AuthDebug;
