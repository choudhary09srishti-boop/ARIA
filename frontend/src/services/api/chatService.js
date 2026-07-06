import client from './client';

export const chatService = {
  async sendMessage(message) {
    const response = await client.post('/chat/', { message });
    return response.data;
  },

  async sendVoiceMessage(transcript) {
    const response = await client.post('/voice/', { transcript });
    return response.data;
  },

  async getHistory(limit = 20) {
    const response = await client.get(`/memory/history?limit=${limit}`);
    return response.data;
  },

  async searchMemory(query) {
    const response = await client.post('/memory/search', { query });
    return response.data;
  },
};