from langgraph.graph import StateGraph,START,END
from typing import TypedDict ,Literal,Annotated
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage,BaseMessage
load_dotenv()
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]  #add_messages is a reducer because without this state will be replaced with new memory always


model= ChatOpenAI(model="gpt-5-mini")

def chat_node(state:ChatState):
    messages=state['messages']
    response=model.invoke(messages)
    return {"messages" : [response]}#cuz messages is a list 



checkpointer=InMemorySaver()

graph=StateGraph(ChatState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot=graph.compile(checkpointer=checkpointer)
