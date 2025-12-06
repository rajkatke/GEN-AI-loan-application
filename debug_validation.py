from graph import create_graph

app = create_graph()

# Mock Input with Invalid PAN
mock_input = {
    "applicant_name": "John Doe",
    "age": 30,
    "gender": "Male",
    "marital_status": "Single",
    "pan_card": "INVALID", # Invalid PAN
    "aadhaar_no": "123456789012",
    "mobile_no": "9876543210",
    "email": "john@example.com",
    "address": "123 Main St",
    "annual_income": 600000,
    "monthly_obligations": 10000,
    "loan_amount": 100000,
    "loan_purpose": "Personal",
    "loan_type": "Personal",
    "employer_name": "Tech Corp",
    "work_experience_years": 5
}

print("Running Validation Test...")
result = app.invoke({"application_data": mock_input})
print("\nWorkflow Result:")
print(result)

if result.get("error"):
    print("\nValidation Failed as expected:")
    print(result["error"])
else:
    print("\nValidation Passed unexpectedly.")
