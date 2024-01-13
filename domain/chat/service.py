from typing import Annotated
from fastapi import Depends
from llm.prompt import Custom_Prompt
from langchain_community.chat_models import ChatOpenAI
from .dto.chat import Chat_Request
from config.config import config

Prompt_Dep = Annotated[Custom_Prompt, Depends(Custom_Prompt)]

class Chat_Service:
    def __init__(self, prompt: Prompt_Dep) -> None:
        self.prompt = prompt

    def get_answer(self, chat_request: Chat_Request) -> str:
        self.prompt.topic = chat_request.topic
        self.prompt.input_text = chat_request.content
        message = self.prompt.create_message()
        chatbot = ChatOpenAI(openai_api_key=config["OPENAI_API_KEY"])
        answer = chatbot(message).content

        return answer
