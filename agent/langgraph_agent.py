# agent/langgraph_agent.py
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

class ReminderState(TypedDict):
    messages: Annotated[list, HumanMessage | AIMessage]

def run_openai(state: ReminderState):
    model = ChatOpenAI(model="gpt-4", temperature=0.3)
    response = model.invoke(state["messages"])
    state["messages"].append(response)
    return state

def build_langgraph():
    workflow = StateGraph(ReminderState)
    workflow.add_node("chat", RunnableLambda(run_openai))
    workflow.set_entry_point("chat")
    workflow.set_finish_point("chat")
    return workflow.compile()
