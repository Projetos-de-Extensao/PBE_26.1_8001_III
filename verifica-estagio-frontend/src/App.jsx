import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Redireciona a rota vazia direto para o login */}
        <Route path="/" element={<Navigate to="/login" />} />
        
        {/* Rota da tela de Login */}
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;