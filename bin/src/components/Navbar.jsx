import React, { useState } from 'react';

export default function ChatSoporte() {
  const [isOpen, setIsOpen] = useState(false);
  const [mensaje, setMensaje] = useState('');
  const [historial, setHistorial] = useState([]);

  const handleEnviar = async () => {
    if (!mensaje.trim()) return;

    // 1. Agrega el mensaje del usuario al historial visual inmediatamente
    const nuevosMensajes = [...historial, { rol: 'usuario', texto: mensaje }];
    setHistorial(nuevosMensajes);
    setMensaje('');

    try {
      // 2. Llama al endpoint de tu server.js (ajusta la URL si es necesario)
      const response = await fetch('http://localhost:3000/api/soporte', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensajeUsuario: mensaje })
      });

      const data = await response.json();

      // 3. Agrega la respuesta de Gemini al historial
      setHistorial([...nuevosMensajes, { rol: 'ia', texto: data.respuesta }]);
    } catch (error) {
      console.error('Error al contactar soporte:', error);
      setHistorial([...nuevosMensajes, { rol: 'ia', texto: 'Error de conexión. Intenta más tarde.' }]);
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      {/* Tu botón existente en el Navbar */}
      <button 
        onClick={() => setIsOpen(!isOpen)} 
        style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer' }}
      >
        Soporte IA <span style={{ color: '#ffb86c' }}>●</span>
      </button>

      {/* Ventana de Chat Flotante */}
      {isOpen && (
        <div style={{
          position: 'absolute', 
          top: '40px', 
          right: '0', 
          width: '300px', 
          background: '#12121c', // Mismo tono oscuro de tu dashboard
          border: '1px solid #333',
          borderRadius: '12px',
          padding: '15px',
          boxShadow: '0 4px 15px rgba(0,0,0,0.5)',
          zIndex: 1000
        }}>
          
          <div style={{ height: '250px', overflowY: 'auto', marginBottom: '10px' }}>
            {historial.map((msg, index) => (
              <div key={index} style={{ 
                marginBottom: '8px', 
                textAlign: msg.rol === 'usuario' ? 'right' : 'left' 
              }}>
                <span style={{
                  display: 'inline-block',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  background: msg.rol === 'ia' ? '#1e1e2d' : '#00d2ff',
                  color: msg.rol === 'ia' ? '#fff' : '#000',
                  fontSize: '14px'
                }}>
                  {msg.texto}
                </span>
              </div>
            ))}
          </div>

          <div style={{ display: 'flex', gap: '5px' }}>
            <input
              type="text"
              value={mensaje}
              onChange={(e) => setMensaje(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleEnviar()}
              placeholder="Escribe tu duda..."
              style={{
                flex: 1,
                padding: '8px',
                borderRadius: '6px',
                border: '1px solid #333',
                background: '#0a0a0f',
                color: '#fff'
              }}
            />
            <button onClick={handleEnviar} style={{
              background: '#00d2ff',
              border: 'none',
              borderRadius: '6px',
              padding: '8px 12px',
              cursor: 'pointer'
            }}>
              <i className="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
