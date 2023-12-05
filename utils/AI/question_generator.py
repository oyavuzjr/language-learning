from django.conf import settings
from typing import List
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser

class Exercises(BaseModel):
    questions: List[str] = Field(description="List of exercises with blank spots")
    answers: List[str] = Field(description="List of answers omitted from the blank spots")


template = """You are a French teacher writing blank completion exercises for your student where blanks are denoted with a "___".
Use the most crucial vocabulary for daily french speaking level.
The topic of the questions: {topic}.
Write 5 questions and answers.
The answers should just be the blank parts of the questions.
{format_instructions}
"""

def generate_question(problem_set):
    
    model = ChatOpenAI()
    parser = PydanticOutputParser(pydantic_object=Exercises)
    prompt = ChatPromptTemplate.from_template(template,partial_variables={"format_instructions": parser.get_format_instructions()})
    chain = prompt | model
    output = chain.invoke({"topic": problem_set.description})
    parsed = parser.invoke(output)
    data =  {
                "questions":parsed.questions,
                "answers":parsed.answers
            }
    print(data)
    return data

