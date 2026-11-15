from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END 
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated, Literal


load_dotenv()

llm = ChatGroq(
            model = 'openai/gpt-oss-120b',
            max_tokens = 700,
            temperature = 0.3
            )

class ChatState(TypedDict):

    messages : Annotated[list[BaseMessage], add_messages]


def chatnode(state : ChatState):

    prompt = f"Act like you are AI ChatBot and answer the user Quesions/Queries {state['messages']}"

    response = llm.invoke(prompt)

    return {'messages' : [response]}

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chatNode", chatnode)

graph.add_edge(START, 'chatNode')
graph.add_edge('chatNode', END)



chatbot = graph.compile(checkpointer=checkpointer)