//새로운 사용자 저장 / 저장된 사용자 정보 가져오기

document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.querySelector('.signup-form');


    const saveUser = (user) => {
        const users = getUsers();
        users.push(user);
        localStorage.setItem('users', JSON.stringify(users));
    };


    const getUsers = () => {
        const users = localStorage.getItem('users');
        return users ? JSON.parse(users) : [];
    };


    const isIdDuplicate = (id) => {
        const users = getUsers();
        return users.some(user => user.id === id);
    };

    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const id = document.getElementById('id').value;
        const password = document.getElementById('password').value;


        if (id.length < 4) {
            alert('아이디는 4자 이상이어야 합니다.');
            return;
        }

        if (password.length < 6) {
            alert('비밀번호는 6자 이상이어야 합니다.');
            return;
        }


        if (isIdDuplicate(id)) {
            alert('이미 사용 중인 아이디입니다.');
            return;
        }

        const newUser = {
            id,
            password,
            createdAt: new Date().toISOString()
        };

        saveUser(newUser);
        alert('회원가입이 완료되었습니다.');
        window.location.href = 'login.html';
    });
});