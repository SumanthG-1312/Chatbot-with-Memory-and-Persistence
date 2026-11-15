import streamlit as st

with st.chat_message('user'):
    st.text('Hi')
with st.chat_message('AI'):
    st.text('Hey, how are you ')