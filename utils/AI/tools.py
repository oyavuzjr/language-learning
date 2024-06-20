from typing import List
from langchain.tools import BaseTool, StructuredTool, tool, Tool
from langchain.output_parsers import PydanticOutputParser, StructuredOutputParser
from utils.AI.question_generator import Exercises
from langchain.pydantic_v1 import BaseModel, Field, validator

# parser = PydanticOutputParser(pydantic_object=Exercises)
# output_parser = StructuredOutputParser.from_response_schemas(Exercises)
# format_instruction = output_parser.get_format_instructions()

class SentenceCompletionArgsSchema(BaseModel):
    questions: List[str] = Field(description="List of exercises with blank spots")
    answers: List[str] = Field(description="List of answers omitted from the blank spots")


# parser = PydanticOutputParser(pydantic_object=Exercises)
# output_parser = StructuredOutputParser.from_response_schemas(Exercises)
# format_instruction = output_parser.get_format_instructions()

class CreateLectureArgsSchema(BaseModel):
    topic:str
    lecture:str

@tool("create_sentence_completion_problems",args_schema=SentenceCompletionArgsSchema)
def create_sentence_completion_problems(questions:List[str], answers:List[str]):
    """
    Create 5 sentence completion problems for the given topic.
    Provide questions where the blank part is '___'
    And provide answers that fill in the blank.
    """
    return({'questions': questions, 'answers': answers})
    return {"success":True}


@tool("create_lecture",args_schema=CreateLectureArgsSchema)
def create_lecture(topic:str,lecture:str):
    """
    Creates a lecture in the topic that the student has requested.
    """
    # return {"success":True}
    return {"topic":topic,"lecture":lecture}




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