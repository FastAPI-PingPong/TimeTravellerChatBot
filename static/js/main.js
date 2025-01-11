document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const chatForm = document.querySelector('.chat-form');
    const logoutBtn = document.querySelector('.logout-btn');
    const sessionList = document.querySelector('.session-list');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const year = document.getElementById('year').value;
        const location = document.getElementById('location').value;
        const persona = document.getElementById('persona').value;

        const yearNum = parseInt(year);
        if (isNaN(yearNum)) {
            alert('연도는 숫자여야 합니다.');
            return;
        }
        if (yearNum < 0 || yearNum > 2024) {
            alert('연도는 0년에서 2024년 사이여야 합니다.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    year: yearNum,
                    location: location,
                    persona: persona
                })
            });
            console.log(response)
            if (response.ok) {
                const data = await response.json();
                session_id = data.id
                console.log(`session_id = ${session_id}`);
                window.location.href = `http://127.0.0.1:8000/static/chat.html?session_id=${session_id}`;
            } else {
                // const error = await response.json();
                alert('세션 생성 중 오류가 발생했습니다.');
            }
        } catch (error) {
            alert('서버 연결 중 오류가 발생했습니다.');
            console.error('Error:', error);
        }
    });

    const fetchRecentSessions = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/session', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const sessions = await response.json();
                if (sessions.length > 0) {
                    sessionList.innerHTML = '';
                    sessions.forEach(session => {
                        const button = document.createElement('button');
                        button.className = 'session-button';
                        button.innerHTML = `
                        <strong>${session.location}, A.D. ${session.year}년</strong>
                        <div class="session-info">${session.persona}</div>
                    `;
                        button.addEventListener('click', () => {
                            window.location.href = `http://127.0.0.1:8000/static/chat.html?session_id=${session.id}`;
                        });
                        sessionList.appendChild(button);
                    });
                } else {
                    const sessionNoneDiv = document.createElement('div');
                    sessionNoneDiv.className = 'session-none';
                    sessionNoneDiv.textContent = '최근 대화 내역이 없습니다.';
                    sessionList.appendChild(sessionNoneDiv);
                }
            }
        } catch (error) {
            console.error('Error fetching sessions:', error);
        }
    };

    fetchRecentSessions();

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        window.location.href = 'login.html';
    });
});