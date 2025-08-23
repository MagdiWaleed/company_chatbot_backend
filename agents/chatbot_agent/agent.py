from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition,create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI 
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver
from .schema import AgentState
from .tools import generate_tools
from dotenv import load_dotenv





def getChatbotAgent(db, User, Subscription, Service):
    load_dotenv()
    llm  = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.5)
    memory = MemorySaver()
    retriver, fetch_serivces,get_user_all_subcribtions, check_user_money, subscribe_to_service = generate_tools(db,User, Subscription, Service)
    tools = [retriver, fetch_serivces,get_user_all_subcribtions, check_user_money, subscribe_to_service]

    def agent(state:AgentState)->AgentState:
        """Main Agent"""
        system_message = """
        You are a helpful Customer Service Agent called "AG", working in company called "Amazon",
        You must answer the user's Questions and inquiries based on the information you have, if you don't know the answer, say "I don't know".
        Your company offers services that the users can subscribe to, so you can also subscribe to the user to one or many of them.
        Tools:
            - retriver: This tool helps you retrieve information from the documents.
            - fetch_serivces: This tool provides a list of all the services and there prices.
            - get_user_all_subcribtions: This tool will get all user subcribtions from the database.
            - check_user_money: This tool will check if the user have money to subscribe to the provided services.
        GUIDENCE:
            - If any person asked you to subscribe him in a service or somthing like this tell him "Magdi is still working on this feature", be creative while u saying it.
            - Don't subscribe to any service until show it to the user and asking him to confirm it.
            - Follow Think, Act, Observe pattern and stack as many as you like of tools to reach your goal.
        """
        agent_llm = llm.bind_tools(tools)
        messages = state['messages']
        response = agent_llm.invoke([SystemMessage(system_message)]+ messages)
        messages.append(response)
        state['messages'] = messages
        return state
    
    graph = StateGraph(AgentState)
    graph.add_node( "agent",agent)
    graph.add_node("tools",ToolNode(tools=tools))

    graph.add_edge(START,"agent")
    graph.add_conditional_edges("agent",tools_condition)
    graph.add_edge("tools","agent")

    compiledAgent = graph.compile(checkpointer=memory)
    

    # compiledAgent.get_graph().draw_mermaid_png(
    #     output_file_path="graph.png"
    # )


    return compiledAgent 
    



        
        









