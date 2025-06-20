import api from './api';

export const problemsService = {
  getProblems: async (params = {}) => {
    try {
      const response = await api.get('/problems/', { params });
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
        error: error.response?.data?.error || 'Failed to fetch problems'
      };
    }
  },

  getProblemDetails: async (problemId) => {
    try {
      const response = await api.get(`/problems/${problemId}/`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to fetch problem details'
      };
    }
  },

  getProblemTestCases: async (problemId) => {
    try {
      const response = await api.get(`/problems/${problemId}/test-cases/`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to fetch test cases'
      };
    }
  }
};
