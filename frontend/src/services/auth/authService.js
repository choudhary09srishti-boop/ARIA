import client from '../api/client';

export const authService = {
  async signup(email, password, fullName) {
    const response = await client.post('/auth/signup', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  async login(email, password) {
    const response = await client.post('/auth/login', {
      email,
      password,
      full_name: '',
    });
    const { access_token } = response.data;
    localStorage.setItem('aria_token', access_token);
    return response.data;
  },

  logout() {
    localStorage.removeItem('aria_token');
    window.location.href = '/login';
  },

  isLoggedIn() {
    return !!localStorage.getItem('aria_token');
  },
};