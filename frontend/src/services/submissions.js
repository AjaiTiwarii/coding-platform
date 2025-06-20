import api from './api';

export const submissionsService = {
  submitCode: async (submissionData) => {
    try {
      const response = await api.post('/submissions/', submissionData);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Submission failed'
      };
    }
  },

  getSubmissions: async (params = {}) => {
    try {
      const response = await api.get('/submissions/', { params });
      return {
        success: true,
        data: response.data,
        pagination: {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to fetch submissions'
      };
    }
  },

  getSubmissionDetails: async (submissionId) => {
    try {
      const response = await api.get(`/submissions/${submissionId}/`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to fetch submission details'
      };
    }
  },

  rejudgeSubmission: async (submissionId) => {
    try {
      const response = await api.post(`/submissions/${submissionId}/rejudge/`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Rejudge failed'
      };
    }
  }
};
