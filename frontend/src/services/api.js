import axios from 'axios';

// Create centralized API instance with proper configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5001',
  withCredentials: true, // Important for CORS with credentials
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000 // 10 second timeout
});

// API request interceptor (for debugging/logging)
api.interceptors.request.use(
  (config) => {
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`);
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
export const sessionStatus = () => api.get('/session-status');

// Data endpoints
export const fetchRiskData = () => api.get('/risk-data');
export const searchRisks = (searchData) => api.post('/search', searchData);
export const addressAutocomplete = (query) => api.get('/address-autocomplete', { params: { query } });

// Health endpoints
export const healthCheck = () => api.get('/health');
export const dbStatus = () => api.get('/db-status');

// Report endpoints
export const downloadReport = (reportData) => api.post('/download-report-direct', reportData);

// Default export
export default api;
