import streamlit as st
import uuid

from langchain_core.messages import HumanMessage, AIMessage
from LangGraph_backend import chatbot

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Session State
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None


# Create New Chat
def new_chat():
    tid = str(uuid.uuid4())

    st.session_state.chats[tid] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.thread_id = tid


# Initialize Chat
if (
    st.session_state.thread_id is None
    or st.session_state.thread_id not in st.session_state.chats
):
    new_chat()


# Sidebar
with st.sidebar:

    st.title("🤖 AI Chatbot")

    if st.button("➕ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.divider()
    st.subheader("💬 Conversation History")

    for tid, chat in reversed(list(st.session_state.chats.items())):

        # Hide empty conversations
        if not chat["messages"]:
            continue

        col1, col2 = st.columns([5, 1])

        with col1:
            if st.button(chat["title"], key=tid, use_container_width=True):
                st.session_state.thread_id = tid
                st.rerun()

        with col2:
            if st.button("🗑️", key=f"del_{tid}"):
                del st.session_state.chats[tid]

                if st.session_state.thread_id == tid:
                    st.session_state.thread_id = None

                st.rerun()


# Current Chat
tid = st.session_state.thread_id
chat = st.session_state.chats[tid]

st.title(chat["title"])


# Display Messages
for msg in chat["messages"]:

    role = "user" if isinstance(msg, HumanMessage) else "assistant"

    with st.chat_message(role):
        st.markdown(msg.content)


# Chat Input
if prompt := st.chat_input("Ask me anything..."):

    # Generate title from first message
    if not chat["messages"]:
        chat["title"] = " ".join(prompt.split()[:5])

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # LangGraph Configuration
    config = {
        "configurable": {
            "thread_id": tid
        }
    }

    # Get AI Response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = chatbot.stream(
                {"messages": [HumanMessage(content=prompt)]},
                config=config
            )

            ai_message = response["messages"][-1]

            st.markdown(ai_message.content)

    # Save Conversation
    chat["messages"] = response["messages"]

    st.rerun()
