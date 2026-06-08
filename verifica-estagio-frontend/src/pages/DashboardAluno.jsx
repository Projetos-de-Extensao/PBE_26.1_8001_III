import React, { useState, useEffect } from 'react';
import api from '../services/api';

export default function DashboardAluno() {
  const [estagios, setEstagios] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    buscarEstagios();
  }, []);

  const buscarEstagios = async () => {
    try {
      // Busca a lista baseada no EstagioSerializer
      const response = await api.get('estagios/');
      setEstagios(response.data);
    } catch (error) {
      console.error('Erro ao buscar estágios:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusStyle = (status) => {
    if (status === 'APROVADO') return 'bg-green-100 text-green-800';
    if (status === 'REPROVADO') return 'bg-red-100 text-red-800';
    return 'bg-yellow-100 text-yellow-800'; // PENDENTE
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center border-b pb-4 mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Bem-vindo, Aluno!</h1>
          <button className="text-red-600 hover:underline font-medium">Sair</button>
        </div>

        <h2 className="text-lg font-semibold mb-4">Meus Estágios:</h2>
        
        {loading ? (
          <p className="text-gray-500">Carregando estágios...</p>
        ) : (
          <div className="overflow-x-auto mb-6">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-100 text-gray-700">
                  <th className="p-3 border-b">ID Empresa</th>
                  <th className="p-3 border-b">Status de Validação</th>
                  <th className="p-3 border-b">Ação</th>
                </tr>
              </thead>
              <tbody>
                {estagios.map((estagio) => (
                  <tr key={estagio.id} className="border-b">
                    {/* O serializer retorna o ID da empresa. Se quiser o nome, o backend precisa serializar aninhado */}
                    <td className="p-3">Empresa #{estagio.empresa}</td> 
                    <td className="p-3">
                      <span className={`px-2 py-1 rounded text-sm font-semibold ${getStatusStyle(estagio.status_validacao)}`}>
                        {estagio.status_validacao || 'PROCESSANDO'}
                      </span>
                    </td>
                    <td className="p-3">
                      <button className="text-blue-600 hover:underline">Ver Detalhes</button>
                    </td>
                  </tr>
                ))}
                {estagios.length === 0 && (
                  <tr>
                    <td colSpan="3" className="p-3 text-center text-gray-500">Nenhum estágio encontrado.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}

        <button className="bg-blue-700 text-white font-bold py-2 px-4 rounded hover:bg-blue-800">
          + Novo Cadastro de Estágio
        </button>
      </div>
    </div>
  );
}