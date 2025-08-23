import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Button, Alert } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { viewLocations, addLocation } from '../services/api';

const LocationDebug = () => {
  const { user, token, loading, isAuthenticated } = useAuth();
  const [debugInfo, setDebugInfo] = useState({
    tokenCheck: null,
    locationCheck: null,
    addTest: null,
    apiUrl: null
  });

  useEffect(() => {
    // Get API URL being used
    setDebugInfo(prev => ({
      ...prev,
      apiUrl: process.env.NODE_ENV === 'production' || window.location.hostname.includes('vercel.app') 
        ? 'https://bioscope-project-production.up.railway.app'
        : process.env.REACT_APP_API_URL || 'http://localhost:5000'
    }));
  }, []);

  const testToken = async () => {
    try {
      console.log('🔑 Testing JWT token status...');
      const tokenFromStorage = localStorage.getItem('auth_token');
      const userFromStorage = localStorage.getItem('user');
      
      setDebugInfo(prev => ({
        ...prev,
        tokenCheck: {
          success: true,
          data: {
            hasToken: !!token,
            hasStoredToken: !!tokenFromStorage,
            hasUser: !!user,
            hasStoredUser: !!userFromStorage,
            tokenPresent: token ? '[PRESENT]' : '[MISSING]',
            storedTokenPresent: tokenFromStorage ? '[PRESENT]' : '[MISSING]'
          },
          status: 200
        }
      }));
    } catch (error) {
      console.error('❌ Token check failed:', error);
      setDebugInfo(prev => ({
        ...prev,
        tokenCheck: {
          success: false,
          error: error.message,
          status: 'Client Error'
        }
      }));
    }
  };

  const testViewLocations = async () => {
    try {
      console.log('🔍 Testing view locations...');
      const response = await viewLocations();
      setDebugInfo(prev => ({
        ...prev,
        locationCheck: {
          success: true,
          data: response.data,
          status: response.status
        }
      }));
    } catch (error) {
      console.error('❌ View locations failed:', error);
      setDebugInfo(prev => ({
        ...prev,
        locationCheck: {
          success: false,
          error: error.response?.data || error.message,
          status: error.response?.status || 'Network Error'
        }
      }));
    }
  };

  const testAddLocation = async () => {
    try {
      console.log('🔍 Testing add location...');
      const testLocation = {
        hotel_name: 'DEBUG TEST HOTEL',
        street_address: '123 Test Street',
        city: 'Princeton',
        zip_code: '07043',
        email: 'debug@test.com'
      };
      const response = await addLocation(testLocation);
      setDebugInfo(prev => ({
        ...prev,
        addTest: {
          success: true,
          data: response.data,
          status: response.status
        }
      }));
    } catch (error) {
      console.error('❌ Add location failed:', error);
      setDebugInfo(prev => ({
        ...prev,
        addTest: {
          success: false,
          error: error.response?.data || error.message,
          status: error.response?.status || 'Network Error'
        }
      }));
    }
  };

  const renderDebugSection = (title, data, color = 'info') => (
    <Paper sx={{ p: 2, mb: 2, bgcolor: '#f5f5f5' }}>
      <Typography variant="h6" sx={{ mb: 1, color: color === 'error' ? 'red' : 'blue' }}>
        {title}
      </Typography>
      {data ? (
        <pre style={{ fontSize: '12px', overflow: 'auto', maxHeight: '200px' }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      ) : (
        <Typography variant="body2" color="textSecondary">
          Click test button to check
        </Typography>
      )}
    </Paper>
  );

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" sx={{ mb: 3, color: 'red' }}>
        🔧 COMPREHENSIVE LOCATION DEBUG
      </Typography>

      {/* Current Auth State */}
      <Paper sx={{ p: 2, mb: 2, bgcolor: '#e3f2fd' }}>
        <Typography variant="h6" sx={{ mb: 1 }}>
          📋 CURRENT AUTH STATE
        </Typography>
        <Typography variant="body2">
          <strong>User:</strong> {user ? JSON.stringify(user) : 'NULL'}
        </Typography>
        <Typography variant="body2">
          <strong>Loading:</strong> {loading ? 'TRUE' : 'FALSE'}
        </Typography>
        <Typography variant="body2">
          <strong>isAuthenticated():</strong> {isAuthenticated() ? 'TRUE' : 'FALSE'}
        </Typography>
        <Typography variant="body2">
          <strong>API URL:</strong> {debugInfo.apiUrl}
        </Typography>
        <Typography variant="body2">
          <strong>Environment:</strong> {process.env.NODE_ENV}
        </Typography>
        <Typography variant="body2">
          <strong>Hostname:</strong> {window.location.hostname}
        </Typography>
      </Paper>

      {/* Test Buttons */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <Button 
          variant="contained" 
          onClick={testToken}
          sx={{ bgcolor: 'orange' }}
        >
          🔑 Test JWT Token
        </Button>
        <Button 
          variant="contained" 
          onClick={testViewLocations}
          sx={{ bgcolor: 'purple' }}
        >
          👀 Test View Locations
        </Button>
        <Button 
          variant="contained" 
          onClick={testAddLocation}
          sx={{ bgcolor: 'green' }}
        >
          ➕ Test Add Location
        </Button>
      </Box>

      {/* Debug Results */}
      {renderDebugSection(
        '🔑 JWT TOKEN CHECK',
        debugInfo.tokenCheck,
        debugInfo.tokenCheck?.success ? 'success' : 'error'
      )}

      {renderDebugSection(
        '👀 VIEW LOCATIONS CHECK',
        debugInfo.locationCheck,
        debugInfo.locationCheck?.success ? 'success' : 'error'
      )}

      {renderDebugSection(
        '➕ ADD LOCATION TEST',
        debugInfo.addTest,
        debugInfo.addTest?.success ? 'success' : 'error'
      )}

      {/* Instructions */}
      <Alert severity="info" sx={{ mt: 2 }}>
        <Typography variant="body2">
          <strong>DEBUG INSTRUCTIONS:</strong><br/>
          1. Click "Test JWT Token" first - this shows if your JWT authentication is working<br/>
          2. Click "Test View Locations" - this tests if you can fetch data with JWT auth<br/>
          3. Click "Test Add Location" - this tests if you can add data with JWT auth<br/>
          4. Share the JSON results with the developer to identify the exact problem
        </Typography>
      </Alert>
    </Box>
  );
};

export default LocationDebug;
