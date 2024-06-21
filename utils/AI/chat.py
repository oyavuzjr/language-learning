from django.conf import settings
from typing import List
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.schema import AIMessage
from langchain import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from dashboard.models import Chat
from .history import DjangoChatMessageHistory  # Import the custom history class
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate
)
from utils.AI.tools import create_lecture, create_sentence_completion_problems, lecture_tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from typing import Dict, Tuple

def setup_memory(chat_id:int) -> Tuple[Dict, ConversationBufferMemory]:
    """
    Sets up memory for the open ai functions agent.
    :return a tuple with the agent keyword pairs and the conversation memory.
    """
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True,chat_memory=DjangoChatMessageHistory(chat_id), input_key='text', output_key="output")

    return agent_kwargs, memory


load_dotenv()

chat = ChatOpenAI(    
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,)

def send_message(chat_id: int, text: str):
    # memory = ConversationBufferMemory(memory_key="messages", return_messages=True, chat_memory=DjangoChatMessageHistory(chat_id))

    prompt = ChatPromptTemplate(
        input_variables=["text", "memory"],
        messages=[
            MessagesPlaceholder(variable_name="memory"),
            SystemMessagePromptTemplate.from_template("You are a French teacher who is teaching an English speaker. You are to provide instructions and explanations in English while the examples and material will be French.\n\nDon't let the student get off topic"),
            HumanMessagePromptTemplate.from_template("{text}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )
    tools = [create_sentence_completion_problems, create_lecture]
    agent = create_openai_tools_agent(chat, tools, prompt)
    agent_kwargs, memory = setup_memory(chat_id)

    agent_executor = AgentExecutor(
        return_intermediate_steps=True,
        agent=agent,
        verbose=True,
        tools=tools,
        agent_kwargs=agent_kwargs,
        memory=memory,
        prompt=prompt
    )


    result = agent_executor({"text": text})
    # result = agent(text)
    print(result)
    return result, result['output']
