from llama_index.core import (StorageContext,VectorStoreIndex,SimpleDirectoryReader)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from langchain_core.runnables import RunnableConfig
import chromadb
from typing import Annotated, List

from dotenv import load_dotenv
print(load_dotenv())

def generate_tools(db, User, Subscription, Service):

    embedd_model = GeminiEmbedding(
        model = 'models/embeddings-001'
    )
    llm = Gemini(model="models/gemini-2.5-flash")
    
    client = chromadb.PersistentClient(path="./agents/chroma_db")
    collection = client.get_or_create_collection("collection")
    vectorStorage = ChromaVectorStore(chroma_collection=collection)
    index = VectorStoreIndex.from_vector_store(vectorStorage, embed_model=embedd_model)
    query_engine = index.as_query_engine(llm=llm)

    def retriver(query:str)->str:
        """This tool helps the agent retrieve information from the documents.
        Args:
            - query: The question to ask for the query engine.
        Returns:
            - The answer to the question.
        Example:
            - query_engine("What is the type of service you have?")
        Note: This tool is used by the agent to retrieve information from the documents.
        """
        return query_engine.query(query).response
    
    def fetch_serivces():
        """This tool gets all the serivces and their prices."""
        servicesObjects = Service.query.all()
        services =[]
        for i,service in enumerate(servicesObjects):
            services.append(f"{i})  Service Name: {service.service_name}, Service Price: {service.service_price}")
        return "\n".join(services)
    
    def get_user_all_subcribtions(config: RunnableConfig = None):
        """This tool list the user subscribtions and user remaining money"""
        user_id = config.get("configurable",{}).get("user_id")
        user = User.query.filter_by(user_id = user_id).first()
        outputString = "User Subscriptions: \n"
        for i,subscription in enumerate(user.subscriptions):
            service = Service.query.filter_by(service_id = subscription.service_id).first()
            outputString+=str(i)+" Name: "+service.service_name+", Price: "+service.service_price+", Category: "+service.category+", Plan Type: "+subscription.plan_type
        return outputString
        
    
    
    def check_user_money(subscribe_to:List[float],config: RunnableConfig = None):
        """This tool check if the user have enough money for the services subscribtions.
        Args:
            -   subscribe_to: a list of the prices of the services the user want to subscribe to.
        """
        user_id = config.get("configurable",{}).get("user_id")
        user_money = User.query.filter_by(user_id = user_id).first().money
        total_price = sum(subscribe_to)
        if user_money<total_price:
            return "The User Don't have enough money"
        else:
            return "The User have enough money"



    
    def subscribe_to_service(services:List[str], planTypes:List[str], config: RunnableConfig = None):
        """This tool enables you to subscribe the user to list of available services.
        Args:
            -   services: List of services names to subscribe too.
            -   planTypes: List of plan types for each service.
        """
        user_id = config.get("configurable",{}).get("user_id")
        user = User.query.filter_by(user_id=user_id).first()
        try:
            for i in range(len(services)):
                service = Service.query.filter_by(service_name=services[i]).first()
                user.money-=service.service_price
                subscription = Subscription(user_id= user_id,service_id= service.service_id, plan_type=planTypes[i])
                db.session.add(subscription)
            if user.money <0:
                return "User Don't have enough money"
            db.session.add(user)
            db.session.commit()
            return f"User Subscribe Successfully, Remaining User Money: {user.money}"
        except Exception as e:
            print("error in subscribing the user: ", e)
            return e


    return retriver, fetch_serivces,get_user_all_subcribtions, check_user_money, subscribe_to_service

