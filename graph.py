from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END
from agents.data_agent import data_agent_node
from agents.risk_agent import risk_agent_node
from agents.compliance_agent import compliance_agent_node
from agents.doc_agent import doc_agent_node
from orchestrator import orchestrator_node
from dotenv import load_dotenv
import os

load_dotenv()

# Define the state
class GraphState(TypedDict):
    application_data: Dict[str, Any]
    enriched_data: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    compliance_result: Dict[str, Any]
    documents: Dict[str, str]
    orchestrator_comment: str
    error: str # For validation errors

def create_graph():
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("data_agent", data_agent_node)
    workflow.add_node("risk_agent", risk_agent_node)
    workflow.add_node("compliance_agent", compliance_agent_node)
    workflow.add_node("doc_agent", doc_agent_node)

    # Define edges
    workflow.set_entry_point("orchestrator")
    workflow.add_edge("orchestrator", "data_agent")
    workflow.add_edge("data_agent", "risk_agent")
    workflow.add_edge("risk_agent", "compliance_agent")
    workflow.add_edge("compliance_agent", "doc_agent")
    workflow.add_edge("doc_agent", END)

    # Compile
    app = workflow.compile()
    return app

if __name__ == "__main__":
    # Test the graph
    app = create_graph()
    
    mock_input = {
        "applicant_name": "John Doe",
        "age": 30,
        "gender": "Male",
        "marital_status": "Single",
        "pan_card": "ABCDE1234F",
        "aadhaar_no": "123456789012",
        "mobile_no": "9876543210",
        "email": "john@example.com",
        "address": "123 Main St",
        "annual_income": 600000,
        "monthly_income": 50000,
        "monthly_obligations": 10000,
        "loan_amount": 100000,
        "loan_purpose": "Personal",
        "loan_type": "Personal",
        "employer_name": "Tech Corp",
        "work_experience_years": 5
    }
    
    print("Running Workflow...")
    result = app.invoke({"application_data": mock_input})
    print("\nWorkflow Result:")
    print(result)
