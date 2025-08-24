from langchain_core.messages import  BaseMessage
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, List

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]
    username: Annotated[str,"user name"]
