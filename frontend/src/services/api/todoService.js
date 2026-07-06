import client from './client';

export const todoService = {
  async getTodos() {
    const response = await client.get('/todos/');
    return response.data;
  },

  async createTodo(title, description = '') {
    const response = await client.post('/todos/', { title, description });
    return response.data;
  },

  async updateTodo(todoId, updates) {
    const response = await client.patch(`/todos/${todoId}`, updates);
    return response.data;
  },

  async deleteTodo(todoId) {
    const response = await client.delete(`/todos/${todoId}`);
    return response.data;
  },
};