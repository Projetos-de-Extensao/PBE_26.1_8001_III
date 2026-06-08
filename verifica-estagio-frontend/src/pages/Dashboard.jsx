import React, { useState, useEffect } from 'react';
import api from '../services/api';

export default function Dashboard() {
  const [contratos, setContratos] = useState([]);
  const [arquivoPdf, setArquivoPdf] = useState(null);
  const [estagioId, setEstagioId] = useState(''); // ID do estágio vinculado
  const [loading, setLoading] = useState(false);

  // Busca os contratos ao carregar a página
  useEffect(() => {
    carregarContratos();
  }, []);

  const carregarContratos = async () => {
    try {
      const response = await api.get('contratos/');
      setContratos(response.data);
    } catch (error) {
      console.error('Erro ao buscar contratos:', error);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!arquivoPdf) return alert('Selecione um arquivo PDF.');

    const formData = new FormData();
    formData.append('arquivo_pdf', arquivoPdf);
    formData.append('estagio', estagioId); 
    // Nota: dependendo da sua API, empresa_id e usuario_id podem ser necessários aqui
    // ou inferidos pelo backend no save() do Contrato.

    setLoading(true);
    try {
      // Como tem arquivo, o Content-Type deve ser multipart/form-data
      await api.post('contratos/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      alert('Contrato enviado com sucesso!');
      setArquivoPdf(null);
      carregarContratos(); // Atualiza a lista após o envio
    } catch (error) {
      console.error('Erro no upload:', error.response?.data);
      alert('Erro ao enviar o contrato. Verifique o console.');
    } finally {
      setLoading(false);
    }
  };

  // Função utilitária para renderizar as cores dos status definidos no seu models.py
  const corStatus = (status) => {
    const cores = {
      RECEBIDO: 'bg-gray-200 text-gray-800',
      PROCESSANDO: 'bg-blue-200 text-blue-800',
      INVALIDO_PENDENTE: 'bg-yellow-200 text-yellow-800',
      VALIDADO_OK: 'bg-green-200 text-green-800',
      APROVADO_FINAL: 'bg-green-500 text-white',
      REPROVADO: 'bg-red-200 text-red-800',
    };
    return cores[status] || 'bg-gray-100 text-gray-600';
  };

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">VerificaEstágio - Dashboard</h1>

      {/* Seção de Upload */}
      <section className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4">Submeter Novo Contrato</h2>
        <form onSubmit={handleUpload} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">ID do Estágio (Provisório):</label>
            <input 
              type="number" 
              value={estagioId} 
              onChange={(e) => setEstagioId(e.target.value)}
              className="border rounded p-2 w-full max-w-xs"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Arquivo PDF:</label>
            <input 
              type="file" 
              accept="application/pdf"
              onChange={(e) => setArquivoPdf(e.target.files[0])}
              className="border rounded p-2 w-full max-w-xs"
            />
          </div>
          <button 
            type="submit" 
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded max-w-xs hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Enviando...' : 'Enviar Contrato'}
          </button>
        </form>
      </section>

      {/* Listagem de Contratos */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Seus Contratos</h2>
        <div className="grid gap-4">
          {contratos.map((contrato) => (
            <div key={contrato.id} className="bg-white p-4 rounded-lg shadow flex justify-between items-center">
              <div>
                <p className="font-medium text-lg">Contrato #{contrato.id}</p>
                <p className="text-sm text-gray-500">Data de Submissão: {new Date(contrato.data_submissao).toLocaleDateString('pt-BR')}</p>
                <p className="text-sm font-semibold mt-1">Score: {contrato.score_conformidade}%</p>
              </div>
              <div className="flex flex-col items-end gap-2">
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${corStatus(contrato.status)}`}>
                  {contrato.status}
                </span>
                <button className="text-blue-600 text-sm hover:underline">
                  Ver Análise Detalhada
                </button>
              </div>
            </div>
          ))}
          {contratos.length === 0 && (
            <p className="text-gray-500 italic">Nenhum contrato submetido ainda.</p>
          )}
        </div>
      </section>
    </div>
  );
}