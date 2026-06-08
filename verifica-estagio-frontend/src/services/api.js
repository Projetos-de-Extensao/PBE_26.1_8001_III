import axios from 'axios';

// Ajuste a URL base para o endereço onde seu backend Django está rodando
const api = axios.create({
  baseURL: 'http://localhost:8000/api/', 
});

// Interceptor para injetar o token de autenticação (quando implementarmos o login)
api.interceptors.request.use((config) => {
 const token = localStorage.getItem('token');
 if (token) {
   config.headers.Authorization = `Token ${token}`;
 }
  return config;
});

export default api;