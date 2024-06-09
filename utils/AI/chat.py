from django.conf import settings
from typing import List
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.schema import AIMessage
from langchain import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate
from dotenv import load_dotenv

template = """You are a French teacher explaining concepts to a student who is an English speaker.
Explain the concepts the student is struggling with in English, providing examples in French.

The student writes to you:
{text}
{format_instructions}
"""

load_dotenv()

chat = ChatOpenAI()

prompt = ChatPromptTemplate(
    input_variables=["text"],
    messages=[
        SystemMessagePromptTemplate.from_template("You are a French teacher explaining concepts to a student who is an English speaker. Explain in English providing examples in French."),
        HumanMessagePromptTemplate.from_template("{text}. Provide response in HTML format."),
    ]
)

chain = LLMChain(
    llm=chat,
    prompt=prompt
)


def send_message(text: str):
    result = chain({"text": text})
    print(result)
    return result["text"]
