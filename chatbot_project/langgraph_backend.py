from langgraph.graph import StateGraph,START,END
from typing import TypedDict ,Literal,Annotated
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage,BaseMessage
load_dotenv()
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]  #add_messages is a reducer because without this state will be replaced with new memory always


model= ChatOpenAI(model="gpt-5-mini")

def chat_node(state:ChatState):
    messages=state['messages']
    response=model.invoke(messages)
    return {"messages" : [response]}#cuz messages is a list 

conn = sqlite3.connect(database= ' chatbot.db', check_same_thread = False)

checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(ChatState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot=graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):   #get me all the checkpoints in the database and from a precific thread id to
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)
