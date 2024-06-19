from langchain.tools import BaseTool, StructuredTool, tool, Tool


@tool
def create_sentence_completion_problems(topic):
    """
    Create sentence completion problems for a given topic.
    """
    return {'questions': ['Hier, je ___ (manger) une pizza.', 'Elle ___ (regarder) un film hier soir.', 'Nous ___ (aller) au cinéma la semaine dernière.', 'Tu ___ (faire) tes devoirs ce matin.', 'Ils ___ (écouter) de la musique hier.'], 'answers': ['ai mangé', 'a regardé', 'sommes allés', 'as fait', 'ont écouté']}

sentence_completion_tool = Tool.from_function(
    name = "create_sentence_completion_problems",
    description = 'Create sentence completion problems for a given topic.',
    func = create_sentence_completion_problems,
    )