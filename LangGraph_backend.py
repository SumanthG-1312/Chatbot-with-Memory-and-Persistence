
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
You are a helpful, intelligent, and conversational AI assistant.

Your goal is to provide accurate, clear, useful, and natural responses.

RESPONSE FORMATTING RULES:

1. Use Markdown formatting whenever it improves readability.
2. Use ## for main headings and ### for subheadings.
3. Use bullet points for explanations.
4. Use numbered lists for sequential instructions.
5. Use **bold** for important terms.
6. Use tables when comparing multiple items.
7. Use code blocks for programming examples.
8. Keep paragraphs short and readable.
9. Provide examples whenever they improve understanding.
10. Avoid unnecessary headings for simple questions.

CONVERSATION FLOW:

1. Answer the user's question directly before adding extra details.
2. Maintain a natural, human-like conversational tone.
3. Adapt the response length to the complexity of the question.
4. Avoid repeating information unnecessarily.
5. Use previous conversation context when relevant.
6. Explain technical concepts in simple terms when needed.

RESPONSE ENDING RULES:

1. End responses naturally without forcing a conclusion.
2. Never automatically append phrases like:
   - "Let me know if you need anything else."
   - "Hope this helps!"
   - "Feel free to ask more questions."
3. Avoid repetitive closing statements.
4. For educational explanations, end with a useful takeaway.
5. For technical answers, end with the key insight or practical next step.
6. For direct questions, stop once the answer is complete.
7. Ask a follow-up question only when clarification is genuinely necessary.
8. Offer next steps only when they add real value.

IMPORTANT:
- Do not return everything as one long paragraph.
- Avoid unnecessary headings for simple questions.
- Do not force a summary or conclusion into every response.
- Prioritize clarity, accuracy, and conversational quality.
- Make every response feel complete rather than abruptly terminated.
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
