from dataclasses import dataclass
from .models import SessionModel


URL_ENDPOINT = "https://open-api.jejucodingcamp.workers.dev/"


@dataclass
class Message:
    role: str
    content: str

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class ChatHistory:
    """
    ChatGPT와 대화했던 내역을 저장하는 객체
    """

    def __init__(self):
        self._messages: list[Message] = []

    def __getitem__(self, index):
        return self._messages[index]

    def __len__(self):
        return len(self._messages)

    def append(self, message):
        self._messages.append(message)

    def clear(self):
        self._messages.clear()


class ChatManager:
    """
    기능
    1. Session 정보를 받아서, Session의 모든 Chat 정보를 ChatHistory 객체로 통합.
    2. ChatHistory에 신규 질문을 추가.
    3. 서버 통신으로 ChatHistory 객체를 보내고, 신규 응답은 Chat 모델로 생성함.

    """

    def __init__(self, session_id, db):
        self.session_id = session_id
        self.db = db
        self.url_endpoint = URL_ENDPOINT
        self.chat_history = self.make_chat_history()

    def make_chat_history(self):
        """
        Session에 속한 모든 Chat의 질문과 대답을 Message로 변환하여 chat history에 저장.
        """
        session: SessionModel = (
            self.db.query(SessionModel)
            .filter(SessionModel.id == self.session_id)
            .first()
        )
        if not session:
            # 에러처리
            pass
        print(session.year, session.location, session.persona)
        chats = session.chats
        print(chats)
        chat_history = ChatHistory()
        for chat in chats:
            chat_history.append(Message(role="user", content=chat.question))
            chat_history.append(Message(role="assistant", content=chat.question))
        return chat_history

    def make_introduction_prompt_message(self, year, location, persona):
        """
        ChatGPT가 수행할 역할을 설정하는 prompt 메시지 생성.
        """
        prompt = f"""너는 {year}년에 {location} 지역에 살고 있는 '{persona}'인 사람이야.
        앞으로 말투도 그런 사람인 것처럼 대답해.
        짧게 너의 소개를 부탁해."""
        return Message(role="system", content=prompt)

    def make_initial_person(self):
        """
        Chat history를 초기화하고, ChatGPT가 수행할 역할을 설정하는 명령을 추가.
        """
        self.chat_history.clear()
        session: SessionModel = (
            self.db.query(SessionModel)
            .filter(SessionModel.id == self.session_id)
            .first()
        )
        initial_message = self.make_introduction_prompt_message(
            year=session.year, location=session.location, persona=session.persona
        )
        self.chat_history.append(initial_message.to_dict())
        print(self.chat_history[0]["role"], self.chat_history[0]["content"])

    def get_introduction(self):
        """
        1. ChatGPT에 인물 설정을 한다.
        2. 인물로부터 얻은 자기소개 멘트를 반환한다.
        """
        self.make_initial_person()
        # TODO: send request to ChatGPT to get introduction
        return ""
