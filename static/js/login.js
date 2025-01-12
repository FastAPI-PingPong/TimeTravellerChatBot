document.addEventListener('DOMContentLoaded', () => {
    const loginFormContainer = document.getElementById('login-form-content');
    const loginMessage = document.getElementById('login-status');
    const loginForm = document.querySelector('.login-form');
    const mainBtn = document.getElementById('main-btn');
    const logoutBtn = document.getElementById('logout-btn');

    const isFromMain = sessionStorage.getItem('fromMain') === 'true';

    if (isFromMain) {
        checkLoginStatus();
    } else {
        showLoginForm();
    }

    window.addEventListener('pageshow', (event) => {
        if (event.persisted) {
            checkLoginStatus();
        }
    });

    mainBtn.addEventListener('click', () => {
        window.location.href = 'main.html';
    });

    function checkLoginStatus() {
        const token = localStorage.getItem('token');

        if (token) {
            loginFormContainer.style.display = 'none';
            loginMessage.style.display = 'block';
        } else {
            showLoginForm();
        }
    }

    function showLoginForm() {
        loginFormContainer.style.display = 'block';
        loginMessage.style.display = 'none';
    }

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        sessionStorage.removeItem('fromMain');
        alert('로그아웃 되었습니다.');
        showLoginForm();
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const id = document.getElementById('id').value;
        const password = document.getElementById('password').value;

        try {
            const formData = new FormData();
            formData.append("username", id);
            formData.append("password", password);

            const response = await fetch('http://127.0.0.1:8000/login', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('refreshToken', data.refresh_token);
                sessionStorage.setItem('fromMain', 'true');
                alert('로그인 성공!');
                window.location.href = 'main.html';
            } else {
                const errorMessage = response.status === 401 ? "아이디 또는 비밀번호가 일치하지 않습니다." : "";
                alert(errorMessage || "로그인 중 오류가 발생했습니다.");
            }
        } catch (error) {
            alert('서버 연결 중 오류가 발생했습니다.');
            console.error('Error:', error);
        }
    });
});