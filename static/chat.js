document.addEventListener('DOMContentLoaded', () => {
    
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
        window.location.href = 'login.html';
        return;
    }

    
    const chatData = JSON.parse(localStorage.getItem('chatData')) || {};
    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.querySelector('.send-btn');
    const logoutBtn = document.querySelector('.logout-btn');
    const introMessage = document.querySelector('.intro-message');

    
    introMessage.textContent = `["안녕하세요! 저는 ${chatData.year || '1800'}년 ${chatData.location || '프랑스'}의 ${chatData.person || '상인'}입니다."]`;

    
    let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

    
    const addMessage = (message, isUser) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    
    chatHistory.forEach(({ text, isUser }) => addMessage(text, isUser));

    
    const sendMessage = () => {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        chatInput.value = '';

        
        chatHistory.push({ text: message, isUser: true });
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));

        // 서버 응답 시뮬레이션 (FastAPI 아직 연결 안함)
        setTimeout(() => {
            const response = `${chatData.person || '인물'}의 답변: ${message}에 대한 답변입니다.`;
            addMessage(response, false);

            chatHistory.push({ text: response, isUser: false });
            localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        }, 1000);
    };


    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    
    logoutBtn.addEventListener('click', () => { //로그아웃 
        localStorage.removeItem('currentUser');
        localStorage.removeItem('chatData');
        localStorage.removeItem('chatHistory');
        window.location.href = 'login.html';
    });
});
