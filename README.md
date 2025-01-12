# TimeTravellerChatBot

![image](logo.png)
ChatGPT API를 통해 과거의 인물에게서 당시의 실감나는 이야기를 들을 수 있습니다!

## 프로젝트 소개

Time Traveller Chat Bot은 과거의 특정 시간과 장소의 인물과 대화할 수 있는 대화형 서비스입니다.
ChatGPT를 활용하여 사용자가 지정한 시대와 지역의 인물로 페르소나를 설정하고, 해당 인물과 역사적 맥락 안에서 대화를 나눌 수 있습니다.

### 주요 기능

- 특정 연도와 지역의 가상 인물과 대화
- historical persona를 통한 그 시대의 뉴스, 경제, 문화, 주요 이슈 등에 대한 대화
- 지속적인 대화 기록 유지
- 사용자 인증 및 개인화된 대화 세션 관리

## 기술 스택

- FastAPI
- SQLAlchemy
- OAuth2 (JWT 인증)
- ChatGPT API
- HTML/CSS/JS(vanilla)

## API 명세

| Method | Endpoint                   | 설명                                          |
| ------ | -------------------------- | --------------------------------------------- |
| POST   | /signup                    | 새로운 사용자 등록                            |
| POST   | /login                     | 사용자 로그인 및 토큰 발급                    |
| POST   | /refresh                   | 사용자 토큰 갱신                              |
| POST   | /session                   | 새로운 대화 세션 생성 (시대, 지역, 인물 설정) |
| GET    | /session                   | 사용자의 대화 세션 목록 조회                  |
| GET    | /introduction/{session_id} | 세션의 초기 자기소개 메시지 조회              |
| POST   | /chat/{session_id}         | 질문 메시지 전송 및 대화 기록 조회            |
| GET    | /chat/{session_id}         | 세션의 모든 대화 내역 조회                    |

## 설치 및 실행 방법

1. 저장소 클론

```bash
git clone [repository-url]
cd time-traveller-chat-bot
```

2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 필요한 환경변수 설정
```

5. 애플리케이션 실행

```bash
uvicorn app.main:app --reload
```

6. 브라우저 실행

http://127.0.0.1:8000/static/login.html 접속

## 사용방법

1. 회원가입 및 로그인하여 액세스 토큰 발급
2. 최근 대화 세션 선택하거나, 새로운 대화 세션 생성 (예: 1800년의 파리의 예술가)
3. 자기소개 메시지 수신하여 인물 확인
4. 해당 시대와 지역에 관련된 질문으로 대화 시작
