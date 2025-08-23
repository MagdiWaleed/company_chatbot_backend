from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, List

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]
