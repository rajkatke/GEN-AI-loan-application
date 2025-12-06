import traceback
from graph import create_graph

try:
    graph = create_graph()
    mock_input = {
        "application_data": {
            "applicant_name": "John Doe",
            "age": 30,
            "gender": "Male",
            "marital_status": "Single",
            "pan_card": "ABCDE1234F",
            "aadhaar_no": "123456789012",
            "mobile_no": "9876543210",
            "email": "john@example.com",
            "address": "123 Main St",
            "employer_name": "Tech Corp",
            "annual_income": 600000,
            "monthly_obligations": 20000,
            "loan_amount": 200000,
            "loan_tenure_years": 2,
            "loan_purpose": "Personal",
            "loan_type": "Personal"
        }
    }
    print("Running Workflow...")
    result = graph.invoke(mock_input)
    print("\nWorkflow Result:")
    # print(result) # Comment out to avoid clutter
    
    if result.get("documents"):
        with open("debug_doc.txt", "w", encoding="utf-8") as f:
            for title, content in result["documents"].items():
                f.write(f"--- {title} ---\n")
                f.write(content)
                f.write("\n\n")
        print("Documents saved to debug_doc.txt")
except Exception:
    traceback.print_exc()
