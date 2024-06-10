from django.conf import settings
from typing import List
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.schema import AIMessage
from langchain import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from dashboard.models import Chat
from .history import DjangoChatMessageHistory  # Import the custom history class

template = """You are a French teacher explaining concepts to a student who is an English speaker.
Explain the concepts the student is struggling with in English, providing examples in French.

The student writes to you:
{text}
{format_instructions}
"""

load_dotenv()

chat = ChatOpenAI()

def send_message(chat_id: int, text: str):
    memory = ConversationBufferMemory(memory_key="messages", return_messages=True, chat_memory=DjangoChatMessageHistory(chat_id))

    prompt = ChatPromptTemplate(
        input_variables=["text", "messages"],
        messages=[
            MessagesPlaceholder(variable_name="messages"),
            SystemMessagePromptTemplate.from_template("You are a French teacher explaining concepts to a student who is an English speaker. Provide HTML response only."),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )

    chain = LLMChain(
        llm=chat,
        prompt=prompt,
        memory=memory,
    )

    result = chain({"text": text})
    print(result)
    return result["text"]
