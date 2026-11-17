import streamlit as st
import uuid

from LangGraph_backend import chatbot
from langchain_core.messages import HumanMessage


# ---------------- Page Configuration ----------------

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ---------------- Utility Functions ----------------

def generate_threadId():
    return str(uuid.uuid4())


def add_thread(thread_id):

    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():

    thread_id = generate_threadId()

    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = []

    add_thread(thread_id)


def load_conversation(thread_id):

    st.session_state["thread_id"] = thread_id

    state = chatbot.get_state(
        {
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    messages = state.values.get("messages", [])

    history = []

    for message in messages:

        if message.type == "human":
            history.append({
                "role": "user",
                "content": message.content
            })

        elif message.type == "ai":
            history.append({
                "role": "assistant",
                "content": message.content
            })

    st.session_state["message_history"] = history


# ---------------- Streaming Function ----------------

def generate_response(user_input):

    config = {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        }
    }

    for message_chunk, metadata in chatbot.stream(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=config,
        stream_mode="messages"
    ):

        if (
            message_chunk.content
            and metadata.get("langgraph_node") == "chat_node"
        ):
            yield message_chunk.content


# ---------------- Session Initialization ----------------

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_threadId()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

add_thread(st.session_state["thread_id"])


# ---------------- Sidebar UI ----------------

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button(" + New Chat", use_container_width=True):
    reset_chat()
    st.rerun()


st.sidebar.header("My Conversations")

for thread_id in st.session_state["chat_threads"]:

    if st.sidebar.button(
        thread_id,
        key=thread_id,
        use_container_width=True
    ):

        load_conversation(thread_id)
        st.rerun()


# ---------------- Main UI ----------------

st.title("AI Assistant")
st.caption("Ask anything. Get structured AI responses.")


# ---------------- Display Conversation History ----------------

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- User Input ----------------

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        ai_message = st.write_stream(
            generate_response(user_input)
        )

    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })