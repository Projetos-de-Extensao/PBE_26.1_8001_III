import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import DashboardAluno from './pages/DashboardAluno';
import EnvioDocumentos from './pages/EnvioDocumentos';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<DashboardAluno />} />
        <Route path="/envio-documentos" element={<EnvioDocumentos />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;