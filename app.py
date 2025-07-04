# app.py
import streamlit as st
from agent.langgraph_agent import build_langgraph
from langchain_core.messages import HumanMessage
from whatsapp.twilio_client import send_whatsapp_reminder

st.set_page_config(page_title="💊 Medication Reminder Agent", layout="centered")

st.title("💊 Medication Reminder Agent")

# LangGraph
agent = build_langgraph()

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = [HumanMessage(content="Hello!")]

user_input = st.text_input("💬 You:", key="user_input")
if st.button("Send"):
    st.session_state.messages.append(HumanMessage(content=user_input))
    state = {"messages": st.session_state.messages}
    updated_state = agent.invoke(state)
    st.session_state.messages = updated_state["messages"]

# Display conversation
for msg in st.session_state.messages:
    st.write(f"**{msg.type.capitalize()}**: {msg.content}")

# Manual Reminder Button
if st.button("📤 Send Reminder Now"):
    send_whatsapp_reminder("💊 Don't forget to take your medicine!")
    st.success("Reminder sent!")
