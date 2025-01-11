document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const chatForm = document.querySelector('.chat-form');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const year = document.getElementById('year').value;
        const location = document.getElementById('location').value;
        const person = document.getElementById('person').value;

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
                    persona: person
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
});