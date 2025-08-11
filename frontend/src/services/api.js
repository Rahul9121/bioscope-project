import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001', // Change this if your Flask backend runs on a different URL
});

export const login = (credentials) => api.post('/login', credentials);
export const fetchRiskData = () => api.get('/risk-data');
