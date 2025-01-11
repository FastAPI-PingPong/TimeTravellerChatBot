document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');
    if (!sessionId) {
        alert('세션 ID가 없습니다.');
        window.location.href = 'main.html';
        return;
    }

    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.querySelector('.chat-input');
    const sendBtn = document.querySelector('.send-btn');
    const logoutBtn = document.querySelector('.logout-btn');
    const introMessage = document.querySelector('.intro-message');

    const addMessage = (message, isUser) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        chatInput.disabled = true;
        sendBtn.disabled = true;

        try {
            addMessage(message, true);
            chatInput.value = '';

            const response = await fetch(`http://127.0.0.1:8000/chat/${sessionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    question: message
                })
            });

            if (response.ok) {
                const chatList = await response.json();
                const lastChat = chatList[chatList.length - 1];
                addMessage(lastChat.answer, false);
            } else {
                alert('메시지 전송 중 오류가 발생했습니다. 마지막 질문은 제거하겠습니다.');
                chatMessages.removeChild(chatMessages.lastChild);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('서버 연결 중 오류가 발생했습니다. 마지막 질문은 제거하겠습니다.');
            chatMessages.removeChild(chatMessages.lastChild);
        } finally {
            chatInput.disabled = false;
            sendBtn.disabled = false;
            chatInput.focus();
        }
    }

    sendBtn.addEventListener('click', () => sendMessage());
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    const fetchIntroduction = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/introduction/${sessionId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data)
                introMessage.textContent = data.answer;
            } else {
                alert('소개 메시지를 가져오는데 실패했습니다.');
                window.location.href = 'main.html';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('서버 연결 중 오류가 발생했습니다.');
        }
    };

    const fetchChatHistory = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/chat/${sessionId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const chatList = await response.json();
                chatList.slice(1).forEach(chat => {
                    addMessage(chat.question, true);
                    addMessage(chat.answer, false)
                });
            } else {
                console.error('채팅 내역을 가져오는데 실패했습니다.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    fetchIntroduction();
    fetchChatHistory();

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        window.location.href = 'login.html';
    });
});
