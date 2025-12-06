# Autonomous Multi-Agent Loan Approval Pipeline

This project implements an autonomous multi-agent system for processing loan applications. It uses 4 specialized AI agents orchestrated to validate data, assess risk, check compliance, and generate documents.

## Architecture

The system follows a sequential pipeline:

1.  **DataAgent**: Ingests application data, validates fields (PAN, Aadhaar), and enriches data with mock external APIs (CIBIL, History).
2.  **RiskAgent**: Calculates financial ratios (DTI, FOIR, LTI), computes a risk score, and assigns a risk tier/interest rate.
3.  **ComplianceAgent**: Checks against regulatory policies (FOIR limit, Loan-to-Income cap, Age limit).
4.  **DocAgent**: Generates the final Sanction Letter or Rejection Letter based on the decision.

## Agents

-   **DataAgent**: `agents/data_agent.py`
-   **RiskAgent**: `agents/risk_agent.py`
-   **ComplianceAgent**: `agents/compliance_agent.py`
-   **DocAgent**: `agents/doc_agent.py`

## Usage

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the Streamlit UI:
    ```bash
    streamlit run app.py
    ```

3.  Fill in the loan application form and click "Submit Application".

## Testing

Run the end-to-end verification script:
```bash
python tests/verify_e2e.py
```

Run individual agent verification:
```bash
python tests/verify_data_agent.py
python tests/verify_risk_agent.py
python tests/verify_compliance_doc.py
```
