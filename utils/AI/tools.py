from langchain.tools import BaseTool, StructuredTool, tool, Tool
from langchain.output_parsers import PydanticOutputParser, StructuredOutputParser
from utils.AI.question_generator import Exercises


# parser = PydanticOutputParser(pydantic_object=Exercises)
# output_parser = StructuredOutputParser.from_response_schemas(Exercises)
# format_instruction = output_parser.get_format_instructions()

@tool
def create_sentence_completion_problems(topic):
    """
    Create sentence completion problems for a given topic.
    """
    print({'questions': ['Hier, je ___ (manger) une pizza.', 'Elle ___ (regarder) un film hier soir.', 'Nous ___ (aller) au cinéma la semaine dernière.', 'Tu ___ (faire) tes devoirs ce matin.', 'Ils ___ (écouter) de la musique hier.'], 'answers': ['ai mangé', 'a regardé', 'sommes allés', 'as fait', 'ont écouté']})

sentence_completion_tool = Tool.from_function(
    name = "create_sentence_completion_problems",
    description = 'Create sentence completion problems for a given topic.',
    func = create_sentence_completion_problems,
    )