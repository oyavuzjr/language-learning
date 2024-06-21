from typing import Dict, Tuple
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate
)
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from utils.AI.history import DjangoChatMessageHistory
from utils.AI.tools import create_lecture, create_sentence_completion_problems, lecture_tool

def setup_memory(chat_id:int) -> Tuple[Dict, ConversationBufferMemory]:
    """
    Sets up memory for the open ai functions agent.
    :return a tuple with the agent keyword pairs and the conversation memory.
    """
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True,chat_memory=DjangoChatMessageHistory(chat_id))

    return agent_kwargs, memory

load_dotenv()

chat = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template("You are a French teacher who is teaching an English speaker. You are to provide instructions and explanations in English while the examples and material will be French."),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [create_sentence_completion_problems, create_lecture]
agent = create_openai_tools_agent(chat, tools, prompt)

agent_kwargs, memory = setup_memory(56)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools,
    agent_kwargs=agent_kwargs,
    memory=memory,
)


# result = agent_executor({"input": "I need to get better at Passe Composé. Teach me"})
result = agent_executor({"input": "I would like some exercises on it."})