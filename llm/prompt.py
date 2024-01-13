from langchain.prompts.chat import ChatPromptTemplate
from enums.topic import Topic
from config.config import config

class Custom_Prompt:
    def __init__(self, topic:Topic|None=None, input_text:str|None=None) -> None:
        self.template = self.generate_template()
        self.topic = topic
        self.input_text = input_text

    def generate_template(self):
        sys_template = config["PROMPT"]
        human_template = "{input_text}" 

        prompt = ChatPromptTemplate.from_messages([
            ("system", sys_template),
            ("human", human_template)
        ])

        return prompt
    
    def create_message(self) -> list:
        message = self.template.format_messages(
            topic=self.topic.name,
            input_text=self.input_text
        )
        return message