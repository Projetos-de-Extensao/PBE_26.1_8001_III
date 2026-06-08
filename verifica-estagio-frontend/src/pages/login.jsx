import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();

  const handleEntrar = (e) => {
    e.preventDefault(); // Impede o navegador de recarregar a página
    navigate('/dashboard'); // Faz o roteamento do React ir para o dashboard
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold text-center text-blue-800 mb-6">
          Plataforma de Gestão de Estágios - Ibmec
        </h1>
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Login</h2>
        
        {/* O onSubmit aqui captura tanto o clique no botão quanto o "Enter" no teclado */}
        <form onSubmit={handleEntrar} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">E-mail ou Matrícula</label>
            <input 
              type="text" 
              placeholder="matricula@alunos.ibmec.edu.br" 
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Senha</label>
            <input 
              type="password" 
              placeholder="*******" 
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button 
            type="submit" 
            className="w-full bg-blue-700 text-white font-bold py-2 px-4 rounded hover:bg-blue-800 mt-2"
          >
            Entrar
          </button>

          <div className="flex items-center justify-between mt-2 text-sm">
            <label className="flex items-center gap-2 text-gray-600">
              <input type="checkbox" className="rounded" />
              Lembrar-me
            </label>
            <a href="#" className="text-blue-600 hover:underline">Esqueci minha senha</a>
          </div>
        </form>
      </div>
    </div>
  );
}