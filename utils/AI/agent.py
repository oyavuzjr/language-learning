from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate
)
from langchain.agents import AgentExecutor, create_openai_tools_agent
from dotenv import load_dotenv
from utils.AI.tools import create_lecture, create_sentence_completion_problems, lecture_tool


load_dotenv()

chat = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template("You are a French teacher who is teaching an English speaker. You are to provide instructions and explanations in English while The examples and material will be French."),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools=[create_sentence_completion_problems,create_lecture]
agent = create_openai_tools_agent(chat, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools
)

result = agent_executor({"input": "I need to get better at Passe Composé. Teach me"})

