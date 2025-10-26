import axiosInstance from './axios';

export const medicationService = {
  getAll: async () => {
    const response = await axiosInstance.get('/api/medications/');
    return response.data;
  },

  getById: async (id) => {
    const response = await axiosInstance.get(`/api/medications/${id}/`);
    return response.data;
  },

  create: async (data) => {
    const response = await axiosInstance.post('/api/medications/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await axiosInstance.put(`/api/medications/${id}/`, data);
    return response.data;
  },

  delete: async (id) => {
    await axiosInstance.delete(`/api/medications/${id}/`);
  },
};