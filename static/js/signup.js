document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.querySelector('.signup-form');

    signupForm.addEventListener('submit', async (e) => {
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

        try {
            const response = await fetch("http://127.0.0.1:8000/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: id,
                    password: password
                })
            });

            if (response.ok) {
                alert('회원가입이 완료되었습니다.');
                window.location.href = 'login.html';
            } else {
                const errorMessage = response.status === 409 ? "해당 ID는 사용할 수 없습니다." : "";
                alert(errorMessage || '회원가입 중 오류가 발생했습니다.');
            }
        } catch (error) {
            alert('서버 연결 중 오류가 발생했습니다.');
            console.error('Error:', error);
        }
    });
});