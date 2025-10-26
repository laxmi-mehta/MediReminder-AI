import axiosInstance from './axios';

export const reminderService = {
  getAll: async (filters = {}) => {
    const response = await axiosInstance.get('/api/reminders/', { params: filters });
    return response.data;
  },

  create: async (data) => {
    const response = await axiosInstance.post('/api/reminders/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await axiosInstance.patch(`/api/reminders/${id}/`, data);
    return response.data;
  },

  delete: async (id) => {
    await axiosInstance.delete(`/api/reminders/${id}/`);
  },

  sendTest: async (id) => {
    const response = await axiosInstance.post(`/api/reminders/${id}/send_test/`);
    return response.data;
  },
};