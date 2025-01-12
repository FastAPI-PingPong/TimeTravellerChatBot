document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');
    if (!sessionId) {
        alert('세션 ID가 없습니다.\n새로운 대화 세션 생성으로 다시 시작합니다.');
        window.location.href = 'main.html';
        return;
    }

    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.querySelector('.chat-input');
    const sendBtn = document.querySelector('.send-btn');
    const logoutBtn = document.querySelector('.logout-btn');
    const introMessage = document.querySelector('.intro-message');

    introMessage.classList.add('intro-loading');

    const createEmptyMessage = () => {
        const emptyMessage = document.createElement('div');
        emptyMessage.className = 'empty-chat-message';
        emptyMessage.textContent = '인물에게 질문을 해서 대화를 시작해보세요!';
        chatMessages.appendChild(emptyMessage);
    };

    const removeEmptyMessage = () => {
        const emptyMessage = chatMessages.querySelector('.empty-chat-message');
        if (emptyMessage) chatMessages.removeChild(emptyMessage);
    };

    const addMessage = (message, isUser) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const createWaitingIndicator = () => {
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingIndicator;
    }

    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        chatInput.disabled = true;
        sendBtn.disabled = true;

        try {
            removeEmptyMessage();

            addMessage(message, true);
            chatInput.value = '';

            const waitingIndicator = createWaitingIndicator();

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
                chatMessages.removeChild(waitingIndicator);
                const chatList = await response.json();
                const lastChat = chatList[chatList.length - 1];
                addMessage(lastChat.answer, false);
            } else {
                const data = await response.json();
                console.error(data.message || `HTTP error status: ${response.status}`);
                alert('메시지 전송 중 오류가 발생했습니다.\n마지막 질문은 제거하겠습니다.');
                chatMessages.removeChild(waitingIndicator);
                chatMessages.removeChild(chatMessages.lastChild);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('서버 연결 중 오류가 발생했습니다.\n마지막 질문은 제거하겠습니다.');
            chatMessages.querySelectorAll('.typing-indicator').forEach(el => el.remove());
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
                introMessage.classList.remove('intro-loading');
                introMessage.textContent = data.answer;
            } else {
                const data = await response.json();
                console.error(data.message || `HTTP error status: ${response.status}`);
                alert('소개 메시지를 가져오는데 실패했습니다.\n새로운 대화 세션 생성으로 다시 시작합니다.');
                window.location.href = 'main.html';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('서버 연결 중 오류가 발생했습니다.\n새로운 대화 세션 생성으로 다시 시작합니다.');
            window.location.href = 'main.html';
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
                if (chatList.length <= 1) createEmptyMessage();
                else removeEmptyMessage();
                chatList.slice(1).forEach(chat => {
                    addMessage(chat.question, true);
                    addMessage(chat.answer, false)
                });
            } else {
                const data = await response.json();
                console.error(data.message || `HTTP error status: ${response.status}`);
                alert('이전 대화 내역 조회에 실패했습니다.\n새로운 대화 세션 생성으로 다시 시작합니다');
                window.location.href = 'main.html';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('서버 연결 중 오류가 발생했습니다.\n새로운 대화 세션 생성으로 다시 시작합니다.');
            window.location.href = 'main.html';
        }
    };

    fetchIntroduction();
    fetchChatHistory();

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        window.location.href = 'login.html';
    });
});
