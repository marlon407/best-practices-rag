import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');

  const [threadId, setThreadId] = useState('');
  const [chat, setChat] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setChat([...chat, { type: 'question', text: question }, { type: 'loading', text: 'Carregando...' }]);
    setQuestion('');
    console.log("threadId", threadId);
    const response = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, thread_id: threadId })
    });
    const data = await response.json();
    console.log(data);
    
    setThreadId(data.thread_id);
    setChat([...chat, { type: 'question', text: question }, { type: 'answer', text: data.answer }]);
  };

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h2>Chat com RAG</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="Digite sua pergunta"
          style={{ width: '80%', padding: 8 }}
        />
        <button type="submit" style={{ padding: 8, marginLeft: 8 }}>Enviar</button>
      </form>
      <div style={{ marginTop: 24 }}>
        <strong>Chat:</strong>
        {chat.map((message, index) => (
          <div key={index} style={{ marginTop: 8, background: message.type === 'question' ? '#f4f4f4' : message.type === 'loading' ? '#e4e4e4' : '#d4d4d4', padding: 12, borderRadius: 4 }}>
            {message.text}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
