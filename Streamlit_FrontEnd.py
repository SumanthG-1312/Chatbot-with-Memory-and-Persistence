import streamlit as st

from LangGraph_backend import chatbot
from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

CONFIG = {
    "configurable": {
        "thread_id": "thread-1"
    }
}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

st.title("AI Assistant")
st.caption("Ask anything. Get structured AI responses.")

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = chatbot.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=CONFIG
            )

            ai_message = response["messages"][-1].content

            st.markdown(ai_message)

    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })