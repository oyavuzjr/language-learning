from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.agents import AgentExecutor, create_openai_tools_agent
from dotenv import load_dotenv

from utils.AI.tools import create_sentence_completion_problems


load_dotenv()

chat = ChatOpenAI()

prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)


tools=[create_sentence_completion_problems]

# agent = OpenAIFunctionsAgent(
#     llm=chat,
#     prompt=prompt,
#     tools=tools
# )

agent = create_openai_tools_agent(chat, tools, prompt)



agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools
)



agent_executor({"input": "Give me Passe compose exercises."})
