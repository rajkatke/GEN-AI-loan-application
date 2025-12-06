from fastmcp import FastMCP
import re
import random

# Create an MCP server
mcp = FastMCP("LoanApprovalTools")

@mcp.tool()
def validate_pan(pan: str) -> bool:
    """Validates the PAN card format."""
    # PAN format: ABCDE1234F
    pattern = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
    return bool(re.match(pattern, pan))

@mcp.tool()
def validate_aadhaar(aadhaar: str) -> bool:
    """Validates the Aadhaar number format."""
    # Aadhaar: 12 digits
    pattern = r"^\d{12}$"
    return bool(re.match(pattern, aadhaar))

@mcp.tool()
def fetch_cibil(pan: str) -> int:
    """Fetches the CIBIL score for a given PAN."""
    # Mock CIBIL score fetching
    last_char = pan[-1]
    if last_char == 'A':
        return 850
    elif last_char == 'B':
        return 750
    elif last_char == 'C':
        return 650
    elif last_char == 'D':
        return 550
    else:
        return random.randint(600, 900)

@mcp.tool()
def calculate_risk_score(cibil_score: int, income: float, loan_amount: float) -> int:
    """Calculates a risk score (0-100) based on CIBIL, income, and loan amount."""
    # Base score from CIBIL (300-900) -> normalized to 0-50
    cibil_component = max(0, (cibil_score - 300) / 600 * 50)
    
    # Income to Loan Ratio component (0-50)
    ratio = income / loan_amount
    if ratio > 0.5:
        ratio_component = 50
    elif ratio > 0.3:
        ratio_component = 30
    elif ratio > 0.1:
        ratio_component = 10
    else:
        ratio_component = 0
        
    return int(cibil_component + ratio_component)

@mcp.tool()
def check_regulations(risk_level: str, loan_amount: float) -> bool:
    """Checks if the loan complies with regulations based on risk and amount."""
    if risk_level == "HIGH" and loan_amount > 50000:
        return False
    return True

if __name__ == "__main__":
    mcp.run()
