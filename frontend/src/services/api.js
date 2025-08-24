import axios from 'axios';

// Determine the correct API URL
const getApiUrl = () => {
  const envUrl = process.env.REACT_APP_API_URL;
  console.log('🔍 Environment API URL:', envUrl);
  console.log('🔍 NODE_ENV:', process.env.NODE_ENV);
  console.log('🔍 Hostname:', window.location?.hostname);
  
  // If environment URL is explicitly set, use it
  if (envUrl) {
    console.log('📡 Using explicit REACT_APP_API_URL:', envUrl);
    return envUrl;
  }
  
  // Production: detect deployment and use appropriate backend URL
  if (process.env.NODE_ENV === 'production' || (typeof window !== 'undefined' && window.location.hostname.includes('vercel.app'))) {
    // You'll need to update this with your actual Railway backend URL after deployment
    const railwayUrl = 'https://your-backend-app-production.up.railway.app';
    console.log('🚀 Production mode - using Railway backend:', railwayUrl);
    return railwayUrl;
  }
  
  // Development: use localhost
  const devUrl = 'http://localhost:5001';
  console.log('🛠️ Development mode - using localhost:', devUrl);
  return devUrl;
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

// API request interceptor (session-based logging)
api.interceptors.request.use(
  (config) => {
    console.log(`🌐 SESSION API Request: ${config.method?.toUpperCase()} ${config.url}`);
    console.log('🍪 Using session-based authentication (cookies)');
    
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
export const login = (credentials) => api.post('/account/login', credentials);
export const register = (userData) => api.post('/account/register', userData);
export const logout = () => api.post('/logout', {});
export const forgotPassword = (data) => api.post('/forgot_password', data);

// Data endpoints
export const fetchRiskData = () => api.get('/risk-data');
export const searchRisks = (searchData) => api.post('/locations/search', searchData);
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
