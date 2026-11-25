
from langgraph.graph import StateGraph, START, END 
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_community.tools import DuckDuckGoSearchRun
import sqlite3
import requests
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
import os


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)


search_tool = DuckDuckGoSearchRun()


@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()



tools = [calculator, search_tool, get_stock_price]
llm_with_tools = llm.bind_tools(tools)

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# -------------------
# 3. State
# -------------------

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# create a node 

def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(tools)

graph = StateGraph(ChatState)

# Register nodes

graph.add_node('chat_node', chat_node)
graph.add_node('tools', tool_node)

# Define edges

graph.add_edge(START, 'chat_node')

graph.add_conditional_edges(
    'chat_node',
    tools_condition
)

graph.add_edge('tools', 'chat_node')

workflow = graph.compile(checkpointer=checkpointer)


config = {
    "configurable": {
        "thread_id": "1"
    }
}

output = workflow.invoke(
    {'messages': [HumanMessage(content='what is 13*49')]},
    config=config
)

print(output['messages'][-1].content) 