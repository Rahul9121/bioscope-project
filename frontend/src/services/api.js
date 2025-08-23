import axios from 'axios';

// Get JWT token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('auth_token');
};

// Determine the correct API URL
const getApiUrl = () => {
  const envUrl = process.env.REACT_APP_API_URL;
  console.log('🔍 Environment API URL:', envUrl);
  console.log('🔍 NODE_ENV:', process.env.NODE_ENV);
  
  // Production: use Railway URL
  if (process.env.NODE_ENV === 'production' || window.location.hostname.includes('vercel.app')) {
    return 'https://bioscope-project-production.up.railway.app';
  }
  
  // Development: use env or localhost
  return envUrl || 'http://localhost:5000';
};

const apiUrl = getApiUrl();
console.log('🌐 Using API URL:', apiUrl);

// Create centralized API instance with proper configuration
const api = axios.create({
  baseURL: apiUrl,
  withCredentials: true, // Important for CORS with credentials
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 15000 // 15 second timeout for Railway
});

// API request interceptor (add JWT token and logging)
api.interceptors.request.use(
  (config) => {
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    
    // Add JWT token to Authorization header if available
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔑 JWT token added to request');
    } else {
      console.log('🚫 No JWT token available');
    }
    
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// API response interceptor (for error handling)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Auth endpoints
export const login = (credentials) => api.post('/login', credentials);
export const register = (userData) => api.post('/register', userData);
export const logout = () => api.post('/logout', {});
export const forgotPassword = (data) => api.post('/forgot_password', data);

// Data endpoints
export const fetchRiskData = () => api.get('/risk-data');
export const searchRisks = (searchData) => api.post('/search', searchData);
export const addressAutocomplete = (query) => api.get('/address-autocomplete', { params: { query } });

// Health endpoints
export const healthCheck = () => api.get('/health');
export const dbStatus = () => api.get('/db-status');

// Location endpoints
export const addLocation = (locationData) => api.post('/locations/add', locationData);
export const viewLocations = () => api.get('/locations/view');
export const editLocation = (locationData) => api.post('/locations/edit', locationData);
export const deleteLocation = (locationData) => api.post('/locations/delete', locationData);

// Report endpoints
export const downloadReport = (reportData) => api.post('/download-report-direct', reportData);

// Default export
export default api;
