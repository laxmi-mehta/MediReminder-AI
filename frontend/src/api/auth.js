import axiosInstance from './axios';

export const authService = {
  login: async (credentials) => {
    const response = await axiosInstance.post('/api/auth/login/', credentials);
    return response.data;
  },

  register: async (userData) => {
    const response = await axiosInstance.post('/api/auth/register/', userData);
    return response.data;
  },

  getUser: async () => {
    const response = await axiosInstance.get('/api/auth/user/');
    return response.data;
  },

  logout: async () => {
    await axiosInstance.post('/api/auth/logout/');
  },
};