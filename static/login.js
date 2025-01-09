document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');
    
    
    const getUsers = () => {    
        const users = localStorage.getItem('users');
        return users ? JSON.parse(users) : [];
    };

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const id = document.getElementById('id').value;
        const password = document.getElementById('password').value;
        
        const users = getUsers();
        const user = users.find(user => user.id === id && user.password === password);
        
        if (user) {
            localStorage.setItem('currentUser', JSON.stringify(user));
            alert('로그인 성공!');
            // 로그인 후 리디렉션 (메인페이지 예정)
            // window.location.href = 'main.html';
        } else {
            alert('아이디 또는 비밀번호가 일치하지 않습니다.');
        }
    });
});
