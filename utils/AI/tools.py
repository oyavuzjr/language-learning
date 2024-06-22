from typing import List
from langchain.tools import BaseTool, StructuredTool, tool, Tool
from langchain.output_parsers import PydanticOutputParser, StructuredOutputParser
from dashboard.models import CompletionQuestion, Lecture, MultipleChoiceQuestion
from utils.AI.question_generator import Exercises
from langchain.pydantic_v1 import BaseModel, Field, validator


class SentenceCompletionArgsSchema(BaseModel):
    question:str = Field(description="Text of the question with blank spot")
    answer: str = Field(description="The answer omitted from the blank spot")

class MultipleChoiceArgsSchema(BaseModel):
    text: str = Field(description="The question text")
    choices: List[str] = Field(description="The 4 unique choices of the multiple choice question")
    correct_answer_index: int = Field(description="The index of the correct answer in the choices list")


class CreateLectureArgsSchema(BaseModel):
    topic:str = Field(description="Topic Of the Lecture")
    lecture:str = Field(description="The markdown body of the lecture text")

@tool("create_sentence_completion_problems",args_schema=SentenceCompletionArgsSchema)
def create_sentence_completion_problems(question:str, answer:str):
    """
    Create a sentence completion problem for the given topic.
    Provide question where the blank part is '___'
    And provide answer that fill in the blank.
    """

    q = CompletionQuestion(correct_answer=answer, text=question)
    q.save()
    ids = [q.id]
    return({'question': question, 'answer': answer,'ids':ids})

@tool("create_multiple_choice_problems",args_schema=MultipleChoiceArgsSchema)
def create_multiple_choice_problems(text:str, choices:List[str], correct_answer_index:int):
    """
    Create a multiple choice question on the given topic
    Provide the choices as a list of strings.
    And provide the index of the correct answer in the choices list.
    """
    q = MultipleChoiceQuestion(choices=choices, text=text,correct_answer=correct_answer_index)
    q.save()
    ids = [q.id]

    return({'ids':ids})


@tool("create_lecture",args_schema=CreateLectureArgsSchema)
def create_lecture(topic:str,lecture:str):
    """
    Creates a lecture in the topic that the student has requested.
    """
    # return {"success":True}
    lec = Lecture.objects.create(text=lecture)
    ids = [lec.id]
    return {"topic":topic,"lecture":lecture,"ids":ids}




sentence_completion_tool = Tool.from_function(
    name = "create_sentence_completion_problems",
    description = """
    Create 5 sentence completion problems for the given topic.
    Provide questions where the blank part is '___'
    And provide answers that fill in the blank.
    """,
    func = create_sentence_completion_problems,
    args_schema=SentenceCompletionArgsSchema,
    return_direct=True
    )


lecture_tool = Tool.from_function(
    name = "create_lecture",
    description = """
    Creates a lecture in the topic that the student has requested.
    """,
    func = create_lecture,
    args_schema=CreateLectureArgsSchema,
    )