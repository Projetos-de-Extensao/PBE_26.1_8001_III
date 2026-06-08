import React, { useState } from 'react';
import api from '../services/api';

export default function EnvioDocumentos({ estagioId }) {
  const [arquivoTCE, setArquivoTCE] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!arquivoTCE) {
      alert('Por favor, selecione o arquivo do TCE em PDF.');
      return;
    }

    // Usamos FormData para lidar com upload de arquivos (multipart/form-data)
    const formData = new FormData();
    formData.append('arquivo_pdf', arquivoTCE);
    
    // O backend exige o vínculo com o estágio (baseado no ContratoSerializer)
    if (estagioId) {
      formData.append('estagio', estagioId);
    }

    setLoading(true);
    try {
      await api.post('contratos/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Documento enviado com sucesso para validação!');
      setArquivoTCE(null); // Limpa o input
    } catch (error) {
      console.error('Erro no upload:', error);
      // Pega a mensagem de erro da API baseada na validação do seu serializer (ex: "O contrato deve ser PDF")
      const msgErro = error.response?.data?.arquivo_pdf || 'Erro ao enviar o arquivo.';
      alert(`Falha no envio: ${msgErro}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-gray-800 border-b pb-4 mb-6">Envio de Documentos</h1>
        
        <form onSubmit={handleUpload} className="flex flex-col gap-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Termo de Compromisso (TCE) em PDF:
            </label>
            <div className="flex items-center gap-3">
              <input 
                type="file" 
                accept="application/pdf"
                onChange={(e) => setArquivoTCE(e.target.files[0])}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" 
              />
            </div>
            {arquivoTCE && (
              <p className="text-sm text-gray-600 mt-2">Selecionado: {arquivoTCE.name}</p>
            )}
          </div>

          <div className="flex justify-end gap-4 mt-4 pt-4 border-t">
            <button 
              type="button" 
              className="text-gray-600 hover:underline font-medium"
              onClick={() => setArquivoTCE(null)}
            >
              Limpar
            </button>
            <button 
              type="submit" 
              disabled={loading}
              className="bg-blue-700 text-white font-bold py-2 px-6 rounded hover:bg-blue-800 disabled:opacity-50"
            >
              {loading ? 'Enviando...' : 'Enviar para Validação'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}