from typing import List
from langchain.tools import BaseTool, StructuredTool, tool, Tool
from langchain.output_parsers import PydanticOutputParser, StructuredOutputParser
from utils.AI.question_generator import Exercises
from pydantic.v1 import BaseModel

# parser = PydanticOutputParser(pydantic_object=Exercises)
# output_parser = StructuredOutputParser.from_response_schemas(Exercises)
# format_instruction = output_parser.get_format_instructions()

class CreateLectureArgsSchema(BaseModel):
    lecture:str

class SentenceCompletionArgsSchema(BaseModel):
    questions:List[str]
    answers:List[str]

@tool("create_sentence_completion_problems",args_schema=SentenceCompletionArgsSchema)
def create_sentence_completion_problems(questions:List[str], answers:List[str]):
    """
    Create 5 sentence completion problems for the given topic.
    Provide questions where the blank part is '___'
    And provide answers that fill in the blank.
    """
    print({'questions': questions, 'answers': answers})
    return {"success":True}


@tool("create_lecture",args_schema=CreateLectureArgsSchema)
def create_lecture(lecture:str):
    """
    Creates a lecture in the topic that the student has requested.
    """
    print(lecture)
    return {"success":True}




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