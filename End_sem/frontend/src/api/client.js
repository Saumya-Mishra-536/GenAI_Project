import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictSingle = async (data) => {
  const response = await apiClient.post('/predict', data);
  return response.data;
};

export const processBatch = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post('/batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const runAgentPlanner = async () => {
  const response = await apiClient.post('/agent/run');
  return response.data;
};

export const getSampleData = async () => {
  const response = await apiClient.get('/data/sample');
  return response.data;
};

export const checkHealth = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

export const checkUploadStatus = async () => {
  const response = await apiClient.get('/upload/status');
  return response.data;
};

export default apiClient;
