from django.conf import settings
from typing import List
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.schema import AIMessage

template = """You are a French teacher explaining concepts to a student who is an English speaker.
Explain the concepts the student is struggling with in English, providing examples in French.

The student writes to you:
{text}
{format_instructions}
"""

def send_message(text: str):
    model = ChatOpenAI()
    parser = CommaSeparatedListOutputParser()
    prompt = ChatPromptTemplate.from_template(template, partial_variables={"format_instructions": parser.get_format_instructions()})
    chain = prompt | model
    output = chain.invoke({"text": text})
    
    # Ensure output is correctly converted to a string
    if isinstance(output, AIMessage):
        output_text = output.content
    else:
        output_text = str(output)
    
    parsed = parser.parse(output_text)
    return parsed[0] if parsed else "No response from AI"
