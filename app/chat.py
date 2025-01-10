from dataclasses import dataclass
from .models import SessionModel, ChatModel
import requests

URL_ENDPOINT = "https://open-api.jejucodingcamp.workers.dev/"


@dataclass
class Message:
    """ChatGPT와 대화했던 개별 질문과 대답을 저장하기 위한 클래스"""

    role: str
    content: str

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class ChatHistory:
    """
    ChatGPT와 대화했던 내역인 Message들을 목록으로 저장하는 객체
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

    def convert_messages_to_dict_list(self):
        return [msg.to_dict() for msg in self._messages]


class ChatManager:
    """
    기능
    1. Session 정보를 받아서, Session의 모든 Chat 정보를 신규 ChatHistory 객체로 통합.
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
        Session에 속한 모든 Chat의 질문과 대답을 Message로 변환하여 chat history에 통합하여 저장.
        모든 신규 질문 요청 전에 반드시 호출되어야 함.
        """
        session: SessionModel = (
            self.db.query(SessionModel)
            .filter(SessionModel.id == self.session_id)
            .first()
        )
        # if not session:
        #     pass
        chat_list: list[ChatModel] = session.chats
        chat_history = ChatHistory()
        if len(chat_list) > 0:
            chat_history.append(
                Message(role="system", content=str(chat_list[0].question))
            )
            chat_history.append(
                Message(role="assistant", content=str(chat_list[0].answer))
            )
            for chat in chat_list[1:]:
                print(f"[Q] {chat.question} [A] {chat.answer}")
                chat_history.append(Message(role="user", content=str(chat.question)))
                chat_history.append(Message(role="assistant", content=str(chat.answer)))
        return chat_history

    def send_question_with_history(self):
        """
        ChatGPT에 chat history가 포함된 질문을 보내고 답변을 받기.
        반환: ChatGPT의 답변 문자열
        """
        messages_dict_list = self.chat_history.convert_messages_to_dict_list()
        response = requests.post(url=self.url_endpoint, json=messages_dict_list)
        # TODO: request 에러처리
        return response.json()["choices"][0]["message"]["content"]

    def add_question_into_history_and_get_answer(self, role, question):
        """신규 질문을 기존 history에 추가한 후, 전체 history를 ChatGPT에게 보내서 답변받기"""

        self.chat_history.append(Message(role=role, content=question))
        answer = self.send_question_with_history()
        return answer

    def create_new_chat(self, question, answer):
        """ChatGPT의 대답 이후, 질문과 대답을 DB에 저장하기 위한 함수"""
        new_chat = ChatModel(
            session_id=self.session_id, question=question, answer=answer
        )
        self.db.add(new_chat)
        self.db.commit()

    def get_introduction(self):
        """ChatGPT가 수행할 역할을 설정하고, 자기소개 멘트를 확보하기"""

        def _make_introduction_prompt_message(year, location, persona):
            """ChatGPT가 수행할 역할을 설정하는 prompt 메시지 생성."""
            prompt = f"""너는 {year}년에 {location} 지역에 살고 있는 '{persona}'인 사람이야.
            앞으로 말투도 그런 사람인 것처럼 대답해.
            짧게 너의 소개를 부탁해."""
            return prompt

        session: SessionModel = (
            self.db.query(SessionModel)
            .filter(SessionModel.id == self.session_id)
            .first()
        )
        introduction_prompt = _make_introduction_prompt_message(
            year=session.year, location=session.location, persona=session.persona
        )
        introduction = self.add_question_into_history_and_get_answer(
            role="system", question=introduction_prompt
        )
        self.create_new_chat(question=introduction_prompt, answer=introduction)
        return introduction

    def get_answer(self, question):
        """ChatGPT에게 질문하고 대답을 얻기"""

        answer = self.add_question_into_history_and_get_answer(
            role="user", question=question
        )
        self.create_new_chat(question=question, answer=answer)
        return answer
