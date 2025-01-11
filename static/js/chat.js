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
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.querySelector('.send-btn');
    const logoutBtn = document.querySelector('.logout-btn');
    const introMessage = document.querySelector('.intro-message');

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

    fetchIntroduction();
});
