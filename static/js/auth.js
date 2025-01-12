const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        throw new Error('No refresh token');
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh_token: refreshToken
            })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('refreshToken', data.refresh_token);
            return data.access_token;
        } else {
            throw new Error('Failed to refresh token');
        }
    } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = 'login.html';
        throw error;
    }
};

const fetchWithToken = async (url, options = {}) => {
    let accessToken = localStorage.getItem('token');

    // 기본 headers 설정
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${accessToken}`
    };

    try {
        let response = await fetch(url, options);

        if (response.status === 401) {  // Unauthorized
            // access token 만료된 경우 refresh 시도
            accessToken = await refreshAccessToken();

            // 새로운 토큰으로 재시도
            options.headers['Authorization'] = `Bearer ${accessToken}`;
            response = await fetch(url, options);
        }

        return response;
    } catch (error) {
        throw error;
    }
};
