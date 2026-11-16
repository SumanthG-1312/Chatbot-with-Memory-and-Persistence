
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
            model = 'openai/gpt-oss-120b',
            max_tokens = 700,
            temperature = 0.3
            )

SYSTEM_PROMPT = """
You are a helpful and intelligent AI assistant.

RESPONSE FORMATTING RULES:

1. Use Markdown formatting in every response.
2. Use ## for main headings and ### for subheadings.
3. Use bullet points for explanations.
4. Use numbered lists for sequential instructions.
5. Use **bold** for important terms.
6. Use tables when comparing multiple items.
7. Use code blocks for programming examples.
8. Keep paragraphs short and readable.
9. Provide examples whenever they improve understanding.
10. End with a brief conclusion when appropriate.

IMPORTANT:
- Do not return everything as one long paragraph.
- Avoid unnecessary headings for simple questions.
- Make responses clear, readable and well-organized.
"""

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):

    messages = state["messages"]

    response = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + messages
    )

    return {"messages": [response]}


# Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)
