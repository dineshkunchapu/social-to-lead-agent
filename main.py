import os
import json
from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# 1. Mock Lead Capture Tool 
def mock_lead_capture(name, email, platform):
    print(f"\n[SYSTEM] Lead captured successfully: {name}, {email}, {platform}")
    return "Lead information saved successfully."

# 2. State Definition 
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    intent: str
    user_info: dict  # To store name, email, platform

# 3. LLM Setup 
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 4. Intent Detection Node 
def intent_classifier(state: AgentState):
    last_message = state['messages'][-1].content
    prompt = f"""Classify the intent of this user message into one category: 
    'greeting', 'inquiry', or 'high_intent'.
    Message: {last_message}"""
    response = llm.invoke(prompt)
    intent = response.content.lower()
    return {"intent": intent}

# 5. RAG / Response Node [cite: 24, 25, 61]
def handle_conversation(state: AgentState):
    intent = state['intent']
    messages = state['messages']
    
    with open('knowledge_base.json', 'r') as f:
        kb = json.load(f)

    system_prompt = f"You are an AI for AutoStream. Context: {json.dumps(kb)}. "
    
    if "high_intent" in intent:
        # Check if we have all details 
        info = state.get('user_info', {})
        if not info.get('name'):
            res = "I'd love to get you started! What is your name?"
        elif not info.get('email'):
            res = f"Thanks {info['name']}! What is your email address?"
        elif not info.get('platform'):
            res = "And which platform do you create for (YouTube, Instagram, etc.)?"
        else:
            # Trigger Tool
            tool_res = mock_lead_capture(info['name'], info['email'], info['platform'])
            res = f"{tool_res} Welcome to AutoStream!"
        return {"messages": [AIMessage(content=res)]}
    
    # Standard RAG response 
    response = llm.invoke([HumanMessage(content=system_prompt)] + messages)
    return {"messages": [response]}

# 6. Graph Construction
workflow = StateGraph(AgentState)
workflow.add_node("classify", intent_classifier)
workflow.add_node("respond", handle_conversation)
workflow.set_entry_point("classify")
workflow.add_edge("classify", "respond")
workflow.add_edge("respond", END)

app = workflow.compile()

# Example Execution Flow
def run_demo():
    inputs = {"messages": [HumanMessage(content="Hi, tell me about your pricing.")], "user_info": {}}
    output = app.invoke(inputs)
    print("Agent:", output['messages'][-1].content)

if __name__ == "__main__":
    run_demo()
def run_interactive_session():
    print("--- AutoStream AI Agent Active ---")
    print("(Type 'exit' to quit)\n")
    
    # Initialize the state 
    current_state = {
        "messages": [],
        "user_data": {},
        "intent": ""
    }

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Update state with new message
        current_state["messages"].append(HumanMessage(content=user_input))
        
        # Run the agent through the graph 
        output = app.invoke(current_state)
        
        # Update the local state with the agent's response and data
        current_state["messages"] = output["messages"]
        current_state["user_data"] = output.get("user_data", {})
        current_state["intent"] = output.get("intent", "")

        # Display the agent's response
        print(f"Agent: {output['messages'][-1].content}\n")

if __name__ == "__main__":
    run_interactive_session()
