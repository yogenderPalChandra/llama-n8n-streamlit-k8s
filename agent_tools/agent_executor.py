

from langchain.agents import initialize_agent, Tool, AgentExecutor, load_agent
from langchain.agents.agent_types import AgentType
from langchain_community.llms import Ollama
from rag_pipeline.query_engine import run_query
from .calculator import calculator
import os

def setup_agent():
    tools = [
        Tool(
            name="Calculator",
            func=calculator,
            description="Useful for math problems. Input must be a valid arithmetic expression."
        ),
        Tool(
            name="RAG Retriever",
            func=lambda q: run_query(q),
            description="Useful when answering question about ingress controller ."
        )
    ]
    llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))

    # agent = load_agent(
    #     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #     tools=tools,
    #     llm=llm,
    #     verbose=True,
    #     handle_parsing_errors=True
    # )

    # agent_executor = AgentExecutor.from_agent_and_tools(
    #     agent=agent,
    #     tools=tools,
    #     max_iterations=1,
    #     verbose=True,
    #     handle_parsing_errors=True
    # )
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True 
    )
    return agent
    #return agent_executor
