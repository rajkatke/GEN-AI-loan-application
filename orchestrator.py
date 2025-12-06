import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from models.schemas import LoanApplication

def orchestrator_node(state: Dict[str, Any]):
    """
    Orchestrator Node.
    Uses Gemini to review the initial application and decide if it's worth processing.
    (In this linear graph, it just logs and passes through, but demonstrates AI agent capability).
    """
    print("--- Phase 0: Orchestration (Orchestrator Agent) ---")
    application_data = state.get("application_data")
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=os.getenv("GEMINI_API_KEY"))
    
    try:
        app = LoanApplication(**application_data)
    except Exception as e:
        # If invalid, we might want to stop here, but for now let's pass it 
        # and let DataAgent handle validation or fail.
        print(f"Orchestrator Warning: Invalid initial data: {e}")
        return {}

    # Ask LLM to review
    messages = [
        HumanMessage(content=f"Review this loan application for {app.applicant_name} requesting {app.loan_amount}. Is this a standard request? Briefly comment.")
    ]
    
    response = llm.invoke(messages)
    print(f"Orchestrator Analysis: {response.content}")
    
    # In a more complex graph, this agent could return a key to route to different paths.
    # For now, it just adds its analysis to the state (if we had a field for it) or just passes.
    
    return {"orchestrator_comment": response.content}
