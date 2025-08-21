import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  withCredentials: true, // Important for CORS with credentials
});

export const login = (credentials) => api.post('/login', credentials);
export const fetchRiskData = () => api.get('/risk-data');
