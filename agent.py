"""
    This module provides functionalities for initializing and managing a file agent.
"""

from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools import ShellTool
from langchain_community.chat_models import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent


def get_file_agent(root_dir: str | None = None):
    """
    Initializes a file management agent.

    Args:
        root_dir (str | None): The root directory for file operations.
            If None, defaults to the current working directory.

    Returns:
        agent: An initialized agent.
    """

    toolkit = FileManagementToolkit(root_dir=root_dir)
    tools = [ShellTool()] + toolkit.get_tools()
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = hub.pull("hwchase17/openai-tools-agent")

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor
