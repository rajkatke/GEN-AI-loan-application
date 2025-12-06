import streamlit as st
import sys
import os
import json
from fpdf import FPDF
import base64

# Add project root to path
sys.path.append(os.getcwd())

from graph import create_graph
from models.schemas import LoanApplication, EnrichedApplication, RiskAssessment, ComplianceResult

st.set_page_config(page_title="HDFC Bank Loan Approval", layout="wide", page_icon="🏦")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background: linear-gradient(90deg, #004c8f 0%, #0073cf 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #003366 0%, #005b9f 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .header-container {
        display: flex;
        align-items: center;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    .logo-img {
        width: 80px;
        margin-right: 20px;
    }
    .header-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(90deg, #004c8f, #0073cf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #eef2f6;
    }
    .sub-header-style {
        font-size: 20px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 20px;
        border-bottom: 2px solid #eef2f6;
        padding-bottom: 10px;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #004c8f;
    }
    </style>
    """, unsafe_allow_html=True)

# Header with Logo
st.markdown("""
    <div class="header-container">
        <img src="https://www.hdfcbank.com/content/api/contentstream-id/723fb80a-2dde-42a3-9793-7ae1be57c87f/05c48619-757c-401d-84e4-f32467d01878/Footer/Resource/HDFC-Bank-logo.png" class="logo-img" alt="HDFC Logo">
        <h1 class="header-title">HDFC BANK Loan Approval System</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar for controls
with st.sidebar:
    st.header("Configuration")
    st.info("This pipeline uses 4 AI Agents to process loan applications.")
    st.markdown("""
    - **DataAgent**: Validates & Enriches Data
    - **RiskAgent**: Calculates Risk Score & Pricing
    - **ComplianceAgent**: Checks Policy Rules
    - **DocAgent**: Generates Sanction/Rejection Letters
    """)

# Main Form
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p class="sub-header-style">New Loan Application</p>', unsafe_allow_html=True)

with st.form("loan_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        applicant_name = st.text_input("Applicant Name", "John Doe")
        age = st.number_input("Age", 18, 70, 30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
        pan_card = st.text_input("PAN Card", "ABCDE1234F")
        aadhaar_no = st.text_input("Aadhaar No", "123456789012")
        mobile_no = st.text_input("Mobile No", "9876543210")
        email = st.text_input("Email", "john@example.com")
        
    with col2:
        address = st.text_area("Address", "123 Main St, City")
        employer_name = st.text_input("Employer Name", "Tech Corp")
        annual_income = st.number_input("Annual Income (₹)", 100000, 10000000, 1200000)
        monthly_obligations = st.number_input("Monthly Obligations (₹)", 0, 500000, 20000)
        loan_amount = st.number_input("Loan Amount (₹)", 10000, 5000000, 500000)
        loan_tenure_years = st.number_input("Tenure (Years)", 1, 30, 2)
        loan_purpose = st.text_input("Purpose", "Personal Use")
        loan_type = st.selectbox("Loan Type", ["Personal", "Business", "Premium", "Digital"])

    submitted = st.form_submit_button("Submit Application")
st.markdown('</div>', unsafe_allow_html=True)

def create_pdf(documents):
    pdf = FPDF()
    for title, content in documents.items():
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, title, ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        # Simple markdown cleanup for PDF and encoding fix
        clean_content = content.replace("**", "").replace("#", "").replace("₹", "Rs. ")
        # Encode to latin-1 compatible text, replacing unknown chars with ?
        clean_content = clean_content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, clean_content)
    return pdf.output(dest='S').encode('latin-1')

if submitted:
    # Create Application Object
    try:
        app_data = {
            "applicant_name": applicant_name,
            "age": age,
            "gender": gender,
            "marital_status": marital_status,
            "pan_card": pan_card,
            "aadhaar_no": aadhaar_no,
            "mobile_no": mobile_no,
            "email": email,
            "address": address,
            "employer_name": employer_name,
            "annual_income": annual_income,
            "monthly_obligations": monthly_obligations,
            "loan_amount": loan_amount,
            "loan_tenure_years": loan_tenure_years,
            "loan_purpose": loan_purpose,
            "loan_type": loan_type
        }
        
        # Run Pipeline
        graph = create_graph()
        
        st.markdown('<p class="sub-header-style">Processing Workflow</p>', unsafe_allow_html=True)
        
        # Workflow Visualization
        st.markdown('<p class="sub-header-style">Processing Status</p>', unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run the graph with streaming to show progress
        final_state = None
        step_count = 0
        total_steps = 5 # Approx
        
        # Map graph keys to display names
        step_mapping = {
            "orchestrator": "Orchestrator Analysis",
            "data_agent": "Data Enrichment",
            "risk_agent": "Risk Assessment",
            "compliance_agent": "Compliance Check",
            "doc_agent": "Document Generation"
        }
        
        for event in graph.stream({"application_data": app_data}):
            for key, value in event.items():
                step_name = step_mapping.get(key, key)
                
                step_count += 1
                progress = min(step_count / total_steps, 1.0)
                progress_bar.progress(progress)
                status_text.info(f"Completed: {step_name} ({int(progress * 100)}%)")
                final_state = value # Update final state with the latest chunk
        
        progress_bar.progress(1.0)
        status_text.success("Pipeline Completed Successfully! (100%)")

        # Display Results
        st.divider()
        st.markdown('<p class="sub-header-style">Pipeline Results</p>', unsafe_allow_html=True)
        
        # Check for validation errors
        # Check for validation errors
        if final_state and final_state.get("error"):
            st.error(final_state["error"])
        else:
            result = graph.invoke({"application_data": app_data})
            
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Enrichment", "⚖️ Risk Assessment", "✅ Compliance", "📄 Documents"])
        
            with tab1:
                st.json(result.get("enriched_data", {}))
                
            with tab2:
                risk_data = result.get("risk_assessment", {})
                col_r1, col_r2 = st.columns(2)
                col_r1.metric("Risk Score", risk_data.get("risk_score", 0))
                col_r1.metric("Risk Tier", risk_data.get("risk_tier", "N/A"))
                col_r2.metric("Interest Rate", f"{risk_data.get('interest_rate')}%" if risk_data.get("interest_rate") else "N/A")
                col_r2.metric("DTI", f"{risk_data.get('dti', 0):.2f}%")
                
                if risk_data.get("is_rejected"):
                    st.error(f"Rejected: {risk_data.get('rejection_reason')}")
                else:
                    st.success("Risk Assessment Passed")
                    
            with tab3:
                comp_data = result.get("compliance_result", {})
                if comp_data.get("is_compliant"):
                    st.success("Compliance Check Passed")
                else:
                    st.error("Compliance Check Failed")
                    for v in comp_data.get("violations", []):
                        st.write(f"- {v}")
                st.metric("Max Eligible Loan", f"₹{comp_data.get('max_eligible_loan', 0)}")

            with tab4:
                documents = result.get("documents", {})
                if documents:
                    for title, content in documents.items():
                        st.subheader(title)
                        st.markdown(content)
                        st.divider()
                    
                    # PDF Download
                    pdf_bytes = create_pdf(documents)
                    st.download_button(
                        label="Download Documents as PDF",
                        data=pdf_bytes,
                        file_name="loan_documents.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.info("No documents generated.")

    except Exception as e:
        st.error(f"Error processing application: {e}")
        st.exception(e)
