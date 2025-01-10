document.addEventListener('DOMContentLoaded', () => {

    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
        window.location.href = 'login.html';
        return;
    }

    const chatForm = document.querySelector('.chat-form');

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const chatData = {
            year: document.getElementById('year').value,
            location: document.getElementById('location').value,
            person: document.getElementById('person').value
        };


        localStorage.setItem('chatData', JSON.stringify(chatData));


        window.location.href = 'chat.html';
    });
});