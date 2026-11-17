# LangGraph Chatbot with Streaming and Conversation Management

A conversational AI chatbot built using LangGraph, Streamlit, and Groq. The application supports real-time response streaming, multiple conversation threads, and conversation restoration using LangGraph's checkpointing mechanism.

## Overview

This project demonstrates how to build a stateful conversational AI application using LangGraph.

Unlike a basic chatbot, this application supports multiple independent conversations. Each conversation is assigned a unique thread ID, allowing LangGraph to maintain separate conversation states.

The Streamlit frontend provides an interactive chat interface with conversation management and progressive AI response rendering.

## Features

- **Conversational AI:** Interact with an LLM through a chat interface.
- **Real-Time Streaming:** Display AI responses progressively instead of waiting for the complete response.
- **Multiple Conversations:** Create and manage independent chat threads.
- **Unique Thread IDs:** Generate UUID-based identifiers for each conversation.
- **Conversation Memory:** Maintain conversation context using LangGraph checkpointing.
- **Conversation Restoration:** Retrieve previous messages using their thread IDs.
- **Interactive UI:** Build a simple and responsive interface using Streamlit.
- **State Management:** Maintain frontend conversation history using Streamlit Session State.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend and user interface |
| LangGraph | Conversation workflow and state management |
| LangChain | LLM integration and message handling |
| Groq | LLM inference |
| UUID | Unique conversation identification |
| InMemorySaver | Conversation checkpointing |

## Project Structure

```text
LangGraph-Chatbot/
│
├── LangGraph_backend.py
│
├── Streamlit_FrontEnd.py
│
├── .env
│
├── requirements.txt
│
└── README.md
