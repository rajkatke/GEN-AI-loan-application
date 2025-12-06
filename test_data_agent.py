from agents.data_agent import data_agent_node
import traceback

try:
    mock_input = {
        "application_data": {
            "application_id": "APP001",
            "applicant_name": "John Doe",
            "pan_card": "ABCDE1234F",
            "aadhaar_no": "123456789012",
            "monthly_income": 50000,
            "loan_amount": 200000,
            "loan_tenure_years": 2,
            "employer_name": "Tech Corp",
            "age": 30,
            "gender": "Male",
            "marital_status": "Single",
            "mobile_no": "9876543210",
            "email": "john@example.com",
            "address": "123 Main St",
            "loan_purpose": "Personal",
            "loan_type": "Personal"
        }
    }
    print("Testing Data Agent...")
    result = data_agent_node(mock_input)
    print("\nData Agent Result:")
    print(result)
except Exception:
    traceback.print_exc()
