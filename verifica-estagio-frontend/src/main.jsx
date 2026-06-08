import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css' // <-- ESTA LINHA É OBRIGATÓRIA!
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)