import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [threadId, setThreadId] = useState('');
  const [chat, setChat] = useState([]);
  const chatContainerRef = useRef(null);

  // Rola para o final quando novas mensagens são adicionadas
  useEffect(() => {
    if (chatContainerRef.current) {
      const scrollToBottom = () => {
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
      };
      scrollToBottom();
      // Adiciona um pequeno delay para garantir que o scroll aconteça após a renderização
      setTimeout(scrollToBottom, 100);
    }
  }, [chat]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newChat = [...chat, { type: 'question', text: question }, { type: 'loading', text: 'Carregando...' }];
    setChat(newChat);
    const response = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, thread_id: threadId })
    });
    const data = await response.json();
    setThreadId(data.threadId);
    setChat([...chat, { type: 'question', text: question }, { type: 'answer', text: data.answer }]);
    setQuestion('');
  };

  return (
    <div style={{ 
      height: '100vh', 
      display: 'flex', 
      flexDirection: 'column',
      fontFamily: 'sans-serif',
      backgroundColor: '#f5f5f5'
    }}>
      <div style={{ 
        padding: '20px', 
        borderBottom: '1px solid #eee',
        backgroundColor: '#fff',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h2 style={{ margin: 0 }}>Chat com RAG</h2>
      </div>

      <div 
        ref={chatContainerRef}
        style={{ 
          flex: 1,
          overflowY: 'auto',
          padding: '20px',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}
      >
        {chat.reverse().map((message, index) => (
          <div 
            key={index} 
            style={{ 
              padding: '12px',
              borderRadius: '8px',
              maxWidth: '80%',
              alignSelf: message.type === 'question' ? 'flex-end' : 'flex-start',
              backgroundColor: message.type === 'question' ? '#007bff' : 
                             message.type === 'loading' ? '#f8f9fa' : '#e9ecef',
              color: message.type === 'question' ? '#fff' : '#000',
              boxShadow: '0 1px 2px rgba(0,0,0,0.1)'
            }}
          >
            {message.text}
          </div>
        ))}
      </div>

      <div style={{ 
        padding: '20px',
        borderTop: '1px solid #eee',
        backgroundColor: '#fff',
        boxShadow: '0 -2px 4px rgba(0,0,0,0.1)'
      }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="Digite sua pergunta"
            style={{ 
              flex: 1,
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #ddd',
              fontSize: '16px',
              outline: 'none'
            }}
          />
          <button 
            type="submit" 
            style={{ 
              padding: '12px 24px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: '#007bff',
              color: '#fff',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={e => e.target.style.backgroundColor = '#0056b3'}
            onMouseOut={e => e.target.style.backgroundColor = '#007bff'}
          >
            Enviar
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
