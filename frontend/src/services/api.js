import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// API Client
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Functions
export const api = {
  // Execute task
  executeTask: async (taskDescription) => {
    const response = await apiClient.post('/execute-task', {
      description: taskDescription,
    });
    return response.data;
  },

  // Get agent status
  getAgentStatus: async () => {
    const response = await apiClient.get('/agent-status');
    return response.data;
  },

  // Get conversation history
  getConversationHistory: async () => {
    const response = await apiClient.get('/conversation-history');
    return response.data;
  },

  // Search memory
  searchMemory: async (query) => {
    const response = await apiClient.get(`/memory/${query}`);
    return response.data;
  },

  // Clear memory
  clearMemory: async () => {
    const response = await apiClient.delete('/memory/clear');
    return response.data;
  },
};

// WebSocket connection
export const connectWebSocket = (onMessage) => {
  const ws = new WebSocket('ws://localhost:8000/ws/agent-stream');

  ws.onopen = () => {
    console.log('WebSocket connected');
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  ws.onclose = () => {
    console.log('WebSocket disconnected');
  };

  return ws;
};

export default api;