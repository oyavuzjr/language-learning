from typing import List
from langchain.tools import BaseTool, StructuredTool, tool, Tool
from langchain.output_parsers import PydanticOutputParser, StructuredOutputParser
from dashboard.models import CompletionQuestion, Lecture
from utils.AI.question_generator import Exercises
from langchain.pydantic_v1 import BaseModel, Field, validator


class SentenceCompletionArgsSchema(BaseModel):
    questions: List[str] = Field(description="List of exercises with blank spots")
    answers: List[str] = Field(description="List of answers omitted from the blank spots")


class CreateLectureArgsSchema(BaseModel):
    topic:str = Field(description="Topic Of the Lecture")
    lecture:str = Field(description="The markdown body of the lecture text")

@tool("create_sentence_completion_problems",args_schema=SentenceCompletionArgsSchema)
def create_sentence_completion_problems(questions:List[str], answers:List[str]):
    """
    Create 5 sentence completion problems for the given topic.
    Provide questions where the blank part is '___'
    And provide answers that fill in the blank.
    """
    ids = []
    for i in range(len(questions)):
        q = CompletionQuestion(correct_answer=answers[i], text=questions[i])
        q.save()
        ids.append(q.id)
        
    return({'questions': questions, 'answers': answers,'ids':ids})
    return {"success":True}


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