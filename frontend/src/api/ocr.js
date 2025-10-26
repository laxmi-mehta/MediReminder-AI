import axiosInstance from './axios';

export const ocrService = {
  upload: async (file) => {
    const formData = new FormData();
    formData.append('image', file);
    
    const response = await axiosInstance.post('/api/ocr/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};